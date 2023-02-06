package bot;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

public class InetBot {
	
	public static void main(String[] args) {
		
		if (args.length < 2) {
			System.err.println("Usage: InetBot <remote.address> <remote.port>");
			System.exit(1);
		}
		
		Socket socket = null;
		BufferedReader socketIn = null;
		PrintWriter socketOut = null;
		BufferedReader sysIn = null;
		
		boolean initOk = false;
		
		try {
			
			socket = new Socket(args[0], Integer.parseInt(args[1]));
			
			socketIn = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			socketOut = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);
			
			sysIn = new BufferedReader(new InputStreamReader(System.in));
			
			initOk = true;
			
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		if (initOk) {
			try {
				
				boolean listen = false;
				
				while ( true ) {
					
					String s = null;
					
					if (listen) {
						s = socketIn.readLine();
					} else {
						s = sysIn.readLine();
					}
					
					if (s == null) break;
					
					if (listen) {
						System.out.print(s + "\n");
					} else {
						socketOut.print(s + "\n");
					}
					
					if (s.equals("go")) {
						if (listen) {
							System.out.flush();
						} else {
							socketOut.flush();
						}
						listen = ! listen;
					}
				}
				
			} catch (IOException e) { }
		}
		
		try {
			if (sysIn != null) {
				sysIn.close();
			}
			if (socketOut != null) {
				socketOut.close();
			}
			if (socketIn != null) {
				socketIn.close();
			}
			if (socket != null) {
				socket.close();
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
}
