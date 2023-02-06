package engine;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;

public class InetBotLauncherServer extends Thread {
	
	private static ServerSocket serverSocket;
	
	private Socket socket;
	private String runningDirectory;
	private List<String> botCommand;
	
	public InetBotLauncherServer(Socket socket, String dir, List<String> bot) {
		this.socket = socket;
		this.runningDirectory = dir;
		this.botCommand = bot;
	}
	
	public static void main(String[] args) {
		
		if (args.length < 2) {
			System.err.println("Usage: InetBotLauncherServer <port> <directory> <bot command with spaces>");
			System.exit(1);
		}
		
		int port = Integer.parseInt(args[0]);
		String runningDirectory = args[1];
		ArrayList<String> botCommand = new ArrayList<String>();
		
		for (int i = 2; i < args.length; i++) {
			botCommand.add(args[i]);
		}
		
		try {
			
			serverSocket = new ServerSocket(port);
			
			System.out.println("Server running on port " + port + ".");
			
			while ( ! isClosed() ) {
				
				Socket soc = serverSocket.accept();
				
				InetBotLauncherServer server = new InetBotLauncherServer(soc, runningDirectory, botCommand);
				server.start();
				
			}
			
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
	
	public void run() {
		
		Process process = null;
		
		BufferedReader socketIn = null;
		PrintWriter socketOut = null;
		BufferedReader processIn = null;
		PrintWriter processOut = null;

		boolean initOk = false;
		
		try {
			
			process = new ProcessBuilder(botCommand).directory(new File(runningDirectory)).start();
	        
			socketIn = new BufferedReader(new InputStreamReader(socket.getInputStream()));
	        socketOut = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);
	        
	        processIn = new BufferedReader(new InputStreamReader(process.getInputStream()));
	        processOut = new PrintWriter(new BufferedWriter(new OutputStreamWriter(process.getOutputStream())), true);

			initOk = true;
			
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		if (initOk) {
			// Redirects Error Stream to /dev/null
	        AsyncStreamConsumer asc = new AsyncStreamConsumer(process.getErrorStream());
			asc.start();
			
			System.out.println("New game started against " + socket.getInetAddress().getCanonicalHostName() + ":" + socket.getPort() + "...");
			
			try {
				
				// Starts by listening.
				boolean listen = true;
				
				while ( true ) {
					
					String s = null;
					
					if (listen) {
						s = socketIn.readLine();
					} else {
						s = processIn.readLine();
					}
					
					if (s == null) break;
					
					if (listen) {
						processOut.print(s + "\n");
					} else {
						socketOut.print(s + "\n");
					}
					
					if (s.equals("go")) {
						if (listen) {
							processOut.flush();
						} else {
							socketOut.flush();
						}
						listen = ! listen;
					}
					
				}
				
			} catch (IOException e) { }
			
			System.out.println("Game against " + socket.getInetAddress().getCanonicalHostName() + ":" + socket.getPort() + " finished.");
		}
				
		try {
			if (processOut != null) {
				processOut.close();
	        }
	        if (processIn != null) {
	        	processIn.close();
	        }
	        if (socketOut != null) {
	        	socketOut.close();
	        }
	        if (socketIn != null) {
	        	socketIn.close();
	        }
	        if (process != null) {
	        	process.destroy();
	        }
	        if (socket != null) {
	        	socket.close();
	        }
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
	
	public static synchronized boolean isClosed() {
		return serverSocket == null || serverSocket.isClosed();
	}
	
	public static synchronized void close() {
		try {
			// Try to close server properly.
			serverSocket.close();
		} catch (IOException e) {
			// Kill the server if we could not close it properly.
			serverSocket = null;
		}
	}

}
