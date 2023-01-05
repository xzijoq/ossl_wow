#pragma once

#if __clang__ || __GNUC__
    #define xzlog_fun __PRETTY_FUNCTION__
#else
    #define xzlog_fun __func__
#endif

#define CompileDebug
#define noFmt

// \033[foregroud(38,2)/bg(48,2) ;r;g;b m
constexpr char xzlog_red_l[] = "\033[0m\033[38;2;0;0;0m\033[48;2;255;88;88m";
constexpr char xzlog_red_w[] = "\033[0m\033[38;2;0;0;255m";
constexpr char xzlog_green_w[] =
    "\033[0m\033[38;2;136;185;136m\033[48;2;8;19;8m";

constexpr char xzlog_yellow_w[] = "\033[0m\033[38;2;255;255;0m";
constexpr char xzlog_clear[]    = "\033[0m";
#define xprMsg( message )                                                       \
    std::cout << xzlog_red_w << message << " ";                                \
    std::cout << xzlog_green_w << xzlog_fun;                                   \
    std::cout << __LINE__ << "\033[0m";                                        \
    std::cout.flush();

#define xprIf( condition, message )                                             \
    do {                                                                       \
        if ( ( condition ) )                                                  \
        {                                                                      \
            std::cout << "\n" << xzlog_yellow_w;                               \
            std::cout << #condition << " <-WARN :\033[0m ";               \
            xprMsg( message );                                                  \
        }                                                                      \
    } while ( false )

#define dieIf( condition, message )                                           \
    do {                                                                       \
        if ( ( condition ) )                                                  \
        {                                                                      \
            std::cout << "\n" << xzlog_red_l;                                  \
            std::cout << #condition << " FAILED:\033[0m ";                     \
            xprMsg( message );                                                  \
            std::cout << "\n";                                                 \
            std::terminate();                                                  \
        }                                                                      \
    } while ( false )

// asd
// printf( "\n\033[31m%s FAILED\033[0m hi %s %s %i ", #condition,       where );
/*
                                                                      \
*/
