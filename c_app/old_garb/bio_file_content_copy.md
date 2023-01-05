#include <openssl/cryptoerr_legacy.h>
#include <openssl/evp.h>
#include <openssl/prov_ssl.h>
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
#include <system_error>
#include <vector>

#include "asio.hpp"
#include "client.h"
#include "openssl/bio.h"
#include "openssl/err.h"
#include "openssl/ssl.h"
#include "server.h"
#include "thread"
using std::cout;
using std::endl;
using std::error_code;
using namespace ::std::placeholders;
using asio::ip::tcp;

int main( int argc, char *argv[] )
{
    BIO *bin  = nullptr;
    BIO *bout = nullptr;
    int  inByte;
    int  outByte;

    std::filesystem::path p1 = __FILE__;
    std::array<char, 512> buffer;
    
    memset( buffer.data(), '\0', buffer.size() );
    cout << p1;
    auto p2 = p1.parent_path();
    auto p3=p2;
    p2/="bio";
    p3/="copy_cat";
    bin  = BIO_new_file( p2.c_str(), "r" );
    bout = BIO_new_file( p3.c_str(), "w" );

    
    prIf( !bin, "suck" );

    
    while ( ( inByte = BIO_read( bin, buffer.data(), buffer.size() ) ) > 0 )
    {
        outByte = BIO_write( bout, buffer.data(), inByte );
        prIf(inByte!=outByte, "inByte "<<inByte<<" outByte: "<<outByte);
    }
    

    BIO_free(bin);
    BIO_free(bout);
    BIO_CLOSE;

    // MAIN ENDS HERE
    prMsg( "\n\nMAIN ENDS HERE" );
    cout << "\n"<<endl;
}
