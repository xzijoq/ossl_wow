struct game4p
{
    int                turn{ 0 };
    int                numplayers{ 0 };
    int                con_index{ 0 };
    std::array<int, 4> pl;
    game4p() { pl.fill( 0 ); }
};
/* #region MemFunc */

void game_loop( game4p& game, int numin, int roll );

void get_inp( game4p& game )
{
    int a = 18;
dumbfuck:
    cout << "\nEnter a num " << game.pl[game.turn] << " Player: " << game.turn
         << " :-> ";
    std::cin >> a;
    if ( a == 11 ) { std::terminate(); }
    if ( a > 10 )
    {
        cout << "\n(1,10) dumbfuck ";
        goto dumbfuck;
    }

    srand( time( 0 ) );
    int roll = rand() % 10;

    game_loop( game, a, roll );
}

void game_loop( game4p& game, int numin, int roll )
{
    if ( numin == 33 )
    {
        game.pl[game.turn] = 101;

        // goto: win and exit
    }
    else
    {
        game.pl[game.turn] += numin;
        // cout<<"\nP"<<game.turn<<" score: "<<game.pl[game.turn];
    }

    if ( game.pl[game.turn] > 100 )
    {
        cout << "\nMotherFucker Number: " << xzlog_red_l << game.turn
             << xzlog_clear << " Wins" << endl;
        return;
    }

    game.turn = ( game.turn + 1 ) % 4;

    get_inp( game );
}
/* #endregion MemFunc */

class session;
class game_cons
{
   public:
    std::array<tcp::socket, 6> pl_socs;
};

struct server
{
    std::vector<game4p> games;
    std::vector<int>    game_emptySlots;

    std::vector<game_cons> cons;
    std::vector<int>       cons_emptySlots;
} serv;

asio::io_context ioc;

tcp::endpoint acp_ep( tcp::v4(), 9002 );
tcp::acceptor acp( ioc, acp_ep );

class session : public std::enable_shared_from_this<session>
{
   public:
    // asio::executor mexc;
    tcp::socket mSoc;
    session() = delete;
    session( tcp::socket&& soc ) : mSoc{ std::move( soc ) } {}
    std::shared_ptr<session> get_shared() { return shared_from_this(); }
};

std::string data;
void Ses_OnRead( std::shared_ptr<session> self, error_code ec, size_t bywr );
void Ses_OnWrite( std::shared_ptr<session> self, error_code ec, size_t bywr )
{
    data = "";
    if ( ec ) { self->mSoc.close(); }
    cout << "GOnWrite" << endl;
    cout << "\nOnWrite use coutn" << self.use_count();

    asio::async_read_until( self->mSoc, asio::dynamic_buffer( data ), '\n',
                            std::bind( &Ses_OnRead, self, _1, _2 ) );
    cout << endl;
}
void Ses_OnRead( std::shared_ptr<session> self, error_code ec, size_t bywr )
{
    if ( ec ) { self->mSoc.close(); }

    cout << "\nOnRead use coutn" << self.use_count();
    cout << "\n the read valie:  \n";
    for ( auto i : data ) { cout << i; }
    cout << "\ndata0:L " << data[0];
    cout << endl;

    switch ( data[0] )
    {
        case 127:
            prMsg( "\nwe are so fucked\n" );
            self->mSoc.close();
            break;
        case '1':
            // create game
            data.clear();
            prMsg( "\nloopback\n" );
            asio::async_write( self->mSoc, asio::buffer( "sucker" ),
                               std::bind( &Ses_OnWrite, self, _1, _2 ) );

            break;
        default:
            data.clear();
            prMsg( "\nBy Default we are fucked\n" );
            prMsg( "\nloopback\n" );
            asio::async_write( self->mSoc,
                               asio::buffer( "\nzzzzzzzzzzzzzzzzzzz.\n" ),
                               std::bind( &Ses_OnWrite, self, _1, _2 ) );
            // self->mSoc.close();
            break;
    }
}

std::weak_ptr<session> dead;
void                   OnAccept( error_code, tcp::socket soc )
{
    // enable ssl?>
    // verify something
    //  ask for previus game id,
    //  ask for a request
    //  create a game
    //  join a unstarted game
    // TODO:  rejoin a game
    // LINK Notes.md#OlaFu
    // ANCHOR: fucketou
    std::string s1{ "your choices are 1. 2. 3. 4. 5." };
    auto        ses = std::make_shared<session>( std::move( soc ) );
    dead            = ses;
    cout << "GOaco" << endl;
    asio::async_write( ses->mSoc, asio::buffer( s1 ),
                       std::bind( &Ses_OnWrite, ses, _1, _2 ) );
}


