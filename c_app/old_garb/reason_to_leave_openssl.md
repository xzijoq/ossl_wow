
#define OPENSSL_NO_DEPRECATED
/* #region Includes */
#include <openssl/core.h>
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
#include "openssl/crypto.h"
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
fs::path append_path( fs::path const& dir, std::string&& file )
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
#include <assert.h>
#include <openssl/bio.h>
#include <openssl/core_names.h>
#include <openssl/err.h>
#include <openssl/evp.h>

#include <memory>
int main( )
{
    unsigned char key[] = "01234567890123456789012345678912";
    unsigned char iv[]  = "0123456789012345";

    unsigned char pt[23] = "plaintext of length 23";
    unsigned char ct[23 + 16];
    unsigned char dt[23];
    unsigned char empty[1] = "";
    unsigned char outtag[16];

    memset( ct, '\0', sizeof( ct ) );
    memset( dt, '\0', sizeof( dt ) );

    int ct_bw{ 0 };
    int dt_bw{ 0 };
    int status{ -19 };
    OSSL_PARAM params[2] = {
        OSSL_PARAM_END, OSSL_PARAM_END
    };

    {
        // Encrypt
        EVP_CIPHER_CTX* ectx = EVP_CIPHER_CTX_new();
        EVP_EncryptInit_ex2( ectx, EVP_chacha20_poly1305(), key, iv,
                                         nullptr );
        EVP_CIPHER_CTX_set_padding(ectx, 0);
        int zero = 0;
        status = EVP_EncryptUpdate( ectx, nullptr, &zero, empty, 0 );
        assert(status == 1);
        assert(zero == 0);

        status = EVP_EncryptUpdate( ectx, ct, &ct_bw, pt, 23 );
		assert(status == 1);

        int bw = ct_bw;

        status = EVP_EncryptFinal_ex( ectx, ct + ct_bw, &ct_bw );
		assert(status == 1);
        ct_bw += bw;

        printf("\nstatus:%i ct_bw:%d\n", status, ct_bw);



        /* Get tag */
        params[0] = OSSL_PARAM_construct_octet_string(OSSL_CIPHER_PARAM_AEAD_TAG,
                                                      outtag, 16);

        status = EVP_CIPHER_CTX_get_params(ectx, params);

        /* Output tag */
        printf("Tag:\n");
        BIO_dump_fp(stdout, outtag, 16);


        EVP_CIPHER_CTX_free( ectx );

        ct[22] = '\0';
    }
    {
        for(auto i = 0; i <16;i++){
          //  outtag[15] ='\0';
        }
        // Decrypt
        EVP_CIPHER_CTX* dctx = EVP_CIPHER_CTX_new();
        EVP_DecryptInit_ex( dctx, EVP_chacha20_poly1305(), nullptr,
                                        key, iv );
        EVP_CIPHER_CTX_set_padding(dctx, 0);
        int zero = 0;
        status = EVP_DecryptUpdate( dctx, nullptr, &zero, empty, 0 );
        assert(status == 1);
        assert(zero == 0);

        status = EVP_DecryptUpdate( dctx, dt, &dt_bw, ct, ct_bw );
		assert(status == 1);

        /* Set expected tag value. */
        params[0] = OSSL_PARAM_construct_octet_string(OSSL_CIPHER_PARAM_AEAD_TAG,
                                                      (void*)outtag, sizeof(outtag));

        status = EVP_CIPHER_CTX_set_params(dctx, params);
        assert(status == 1);

        status = EVP_DecryptFinal_ex( dctx, dt + dt_bw, &dt_bw );



        //decrypts sucsessfully, with sucsess status code of 1
        //https://www.openssl.org/docs/man3.1/man3/EVP_EncryptInit.html in return values
        //does not verify tag, or write it anywhere
        printf("\nstatus:%i decrypted_test:%s\n",status,dt);

        EVP_CIPHER_CTX_free( dctx );
    }
}

// When decrypting, the return value of EVP_DecryptFinal() or EVP_CipherFinal()
// indicates whether the operation was successful. If it does not indicate
// success, the authentication operation has failed and any output data MUST NOT
// be used as it is corrupted.

// EVP_DecryptInit_ex() and EVP_DecryptUpdate() return 1 for success and 0 for
// failure.EVP_DecryptFinal_ex() returns 0 if the decrypt failed or 1 for
// success.