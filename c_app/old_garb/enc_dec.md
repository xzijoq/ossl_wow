

/* #region Includes */
#include <openssl/cryptoerr_legacy.h>
#include <openssl/evp.h>
#include <openssl/prov_ssl.h>
#include <openssl/types.h>
#include <xzlog.h>

#include <algorithm>
#include <array>
#include <asio/buffer.hpp>
#include <asio/executor.hpp>
#include <asio/io_context.hpp>
#include <asio/ip/tcp.hpp>
#include <asio/read.hpp>
#include <asio/write.hpp>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <exception>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iostream>
#include <memory>
#include <string>
#include <string_view>
#include <system_error>
#include <vector>

#include "asio.hpp"
#include "client.h"
#include "openssl/bio.h"
#include "openssl/err.h"
#include "openssl/ssl.h"
#include "server.h"
#include "thread"
/* #endregion */

/* #region using shit */
using std::cout;
using std::endl;
using std::error_code;
using namespace ::std::placeholders;
using asio::ip::tcp;
using std::filesystem::path;
namespace fs = std::filesystem;
/* #endregion */

/* #region Ranfunck */
fs::path append_path( fs::path const &dir, std::string &&file )
{
    path ret;
    ret = dir;
    ret.append( file );
    dieIf( !fs::exists( ret ), "ret: " << ret );
    return ret;
}

/* #endregion Ranfunck */
/* #region clas */

constexpr int AES_BLOCK_SIZE = EVP_MAX_BLOCK_LENGTH;

class data
{
   public:
    std::string key{ "01234567890123456789012345678912" };
    std::string iv{ "0123456789012345" };
    std::string pt{
        "this is the plaintext to be encrypted with the algorithm aes-1281" };
    std::string ct;
    std::string dtx;

    int ct_bwr;
    int dt_bwr;
};
void print3( data const &dt, std::string const &message = "" )
{
    std::cout << message << std::endl;
    cout << "pt: " << dt.pt << endl;
    cout << "ct: " << dt.ct << endl;
    cout << "dt: " << dt.dtx << endl;
    cout << "ct_bwr:  " << dt.ct_bwr;
    cout << " dt_bwr:  " << dt.dt_bwr << endl;
    cout << "ct.(): " << dt.ct.size();
    cout << " dt.(): " << dt.dtx.size();
    cout << " ptt.(): " << dt.pt.size();
}

int main( int argc, char *argv[] )
{
    data dt;
    {
        std::unique_ptr<EVP_CIPHER_CTX, decltype( &::EVP_CIPHER_CTX_free )> ctx(
            EVP_CIPHER_CTX_new(), &::EVP_CIPHER_CTX_free );
        //auto cipher=EVP_chacha20_poly1305();
        auto cipher = EVP_CIPHER_fetch( nullptr, "CHACHA20-POLY1305", nullptr );
        dieIf(!cipher, "prolly wrong algo name");
        print3( dt, "\nstart:" );
        EVP_EncryptInit_ex2( ctx.get(), cipher, (unsigned char *)dt.key.data(),
                             (unsigned char *)dt.iv.data(), nullptr );
        xprMsg("\n"<<EVP_CIPHER_CTX_get_block_size(ctx.get()));
        cout << endl;
        dt.ct.resize( dt.pt.size() + AES_BLOCK_SIZE );
        EVP_EncryptUpdate( ctx.get(), (unsigned char *)dt.ct.data(), &dt.ct_bwr,
                           (const unsigned char *)dt.pt.data(),
                           (int)dt.pt.size() );

        print3( dt, "\nupdate" );
        // int cts_au=dt.ct_bwr;
        //EVP_CIPHER_free( cipher );
        //EVP_CIPHER_free( cipher );
        EVP_EncryptFinal( ctx.get(), (unsigned char *)dt.ct.data() + dt.ct_bwr,
                          &dt.ct_bwr );
        //EVP_CIPHER_CTX_free(ctx.get());
        // print3(dt,"\nfinal");
    }
    {
        std::unique_ptr<EVP_CIPHER_CTX, decltype( &::EVP_CIPHER_CTX_free )>
            dctx( EVP_CIPHER_CTX_new(), &::EVP_CIPHER_CTX_free );

        EVP_DecryptInit_ex( dctx.get(), EVP_chacha20_poly1305(), nullptr,
                            (unsigned char *)dt.key.data(),
                            (unsigned char *)dt.iv.data() );

        dt.dtx.resize( dt.pt.size() + AES_BLOCK_SIZE );
        EVP_DecryptUpdate( dctx.get(), (unsigned char *)dt.dtx.data(),
                           &dt.dt_bwr, (const unsigned char *)dt.ct.data(),
                           (int)dt.ct.size() );
        print3( dt, "\nudinm" );
        EVP_DecryptFinal( dctx.get(),
                          (unsigned char *)dt.dtx.data() + dt.dt_bwr,
                          &dt.dt_bwr );
        //EVP_CIPHER_CTX_cleanup(dctx.get());
        xprMsg( "\n\nMAIN ENDS HERE" );
        cout << "\n" << endl;
    }
}
