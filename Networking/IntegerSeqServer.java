import java.io.PrintWriter;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

class IntegerSeqServer
{
   public static void main( String[] args ) {
        try {
            ServerSocket listen = new ServerSocket( Integer.parseInt(args[0]) );
            System.out.println("Server port is " + listen.getLocalPort() );

            /* handle one client at a time */
            while ( true ) {

                Socket sock = listen.accept();

                /* data from client */
                Scanner rd = new Scanner(sock.getInputStream());

                /* data to client */
                PrintWriter pw = new PrintWriter(sock.getOutputStream(), true);

                System.out.println("Accepted connection from "
                     + sock.getInetAddress() + " at port "
                     + sock.getPort() );
                int count = 0;
                while ( rd.hasNextLine() ) {
                    int line = Integer.parseInt(rd.nextLine());
                    if((line %13) == 0 || (line%31)==0) {
                    count ++;
                    System.out.println( line );
                    }
                    if(line == -1) {
                        String Holder = String.valueOf(count);
                        pw.write(Holder);
                        pw.flush();
                        System.out.println( "closing" + sock );
                        sock.close(); // clean up required
                        break;
                    }
                }

            }
        }
        catch( IOException e ) {
            System.out.println("error: " + e );
        }
    }


}
