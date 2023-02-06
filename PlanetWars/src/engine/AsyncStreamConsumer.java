package engine;

import java.io.IOException;
import java.io.InputStream;

public class AsyncStreamConsumer extends Thread {
	
	private InputStream in;
	
	public AsyncStreamConsumer(InputStream in) {
		this.in = in;
	}
	
	public void run() {
		try {
			while ( in.read() >= 0 ) { }
		} catch (IOException e) { }
	}
	
}
