package snakegame;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.Random;

import javax.swing.ImageIcon;
import javax.swing.JPanel;
import javax.swing.Timer;

public class Mypanel extends JPanel implements KeyListener, ActionListener {
	ImageIcon title = new ImageIcon("title.jpg");
	ImageIcon body = new ImageIcon("body.png");
	ImageIcon up = new ImageIcon("up.png");
	ImageIcon down = new ImageIcon("down.png");
	ImageIcon left = new ImageIcon("left.png");
	ImageIcon right = new ImageIcon("right.png");
	ImageIcon food = new ImageIcon("food.png");
	
	int len;
	int score;
	int[] snakex = new int[700];
	int[] snakey = new int[700];
	String direction;  // U, R, D, L
	boolean isStarted = false;
	boolean isFailed = false;
	Timer timer = new Timer(100, this);
	int foodx;
	int foody;
	Random rand = new Random();
	
	public Mypanel() {
		initSnake();
		this.setFocusable(true);  // 可以获取键盘事件
		this.addKeyListener(this);
		timer.start();
	}

	public void paintComponent(Graphics g) {
		super.paintComponent(g);
		this.setBackground(Color.WHITE);
		title.paintIcon(this, g, 25, 11);
		g.setColor(new Color(30, 30, 30));
		g.fillRect(25, 75, 850, 500);
		g.setColor(Color.WHITE);
		g.drawString("Length: " + len, 750, 35);
		g.drawString("Score: " + score, 750, 50);
		
		if (direction == "U") {
			up.paintIcon(this, g, snakex[0], snakey[0]);
		}
		else if (direction == "R") {
			right.paintIcon(this, g, snakex[0], snakey[0]);			
		}
		else if (direction == "D") {
			down.paintIcon(this, g, snakex[0], snakey[0]);			
		}
		else if (direction == "L") {
			left.paintIcon(this, g, snakex[0], snakey[0]);			
		}
		for (int i = 1; i < len; i ++ ) {
			body.paintIcon(this, g, snakex[i], snakey[i]);
		}
		
		food.paintIcon(this, g, foodx, foody);
		
		if (!isStarted) {
			g.setColor(Color.WHITE);
			g.setFont(new Font("arial", Font.BOLD, 40));
			g.drawString("Press space to start", 260, 300);
		}
		if (isFailed) {
			g.setColor(Color.RED);
			g.setFont(new Font("arial", Font.BOLD, 40));
			g.drawString("Failed: Press space to restart", 170, 300);
		}
	}
	
	public void initSnake() {
		len = 3;
		score = 0;
		direction = "R";
		for (int i = 0; i < len; i ++ ) {
			snakex[i] = 100 - i * 25;  // picture: 25x25
			snakey[i] = 100;
		}
		foodx = 25 + 25 * rand.nextInt(34);  // [0,33]
		foody = 75 + 25 * 2 + 25 * rand.nextInt(20 - 2);
	}
	
	public void moveSnake() {
		for (int i = len - 1; i > 0; i -- ) {
			snakex[i] = snakex[i - 1];
			snakey[i] = snakey[i - 1];
		}
		if (direction == "U") {
			snakey[0] -= 25;
			if (snakey[0] < 75) snakey[0] = 550;
		}
		else if (direction == "R") {
			snakex[0] += 25;
			if (snakex[0] > 850) snakex[0] = 25;
		}
		else if (direction == "D") {
			snakey[0] += 25;
			if (snakey[0] > 550) snakey[0] = 75;
		}
		else if (direction == "L") {
			snakex[0] -= 25;
			if (snakex[0] < 25) snakex[0] = 850;
		}
	}
	
	public boolean isFoodInSnake() {
		for (int i = 0; i < len; i ++ ) {
			if (snakex[i] == foodx && snakey[i] == foody) return true;
		}
		return false;
	}

	@Override
	public void keyPressed(KeyEvent e) {
		int keyCode = e.getKeyCode();
		if (keyCode == KeyEvent.VK_SPACE) {
			if (isFailed) {
				isFailed = false;
				initSnake();
			}
			else isStarted = !isStarted;
			repaint();
		}
		else if (keyCode == KeyEvent.VK_UP) {
			if (direction == "L" || direction == "R") direction = "U";
		}
		else if (keyCode == KeyEvent.VK_RIGHT) {
			if (direction == "U" || direction == "D") direction = "R";
		}
		else if (keyCode == KeyEvent.VK_DOWN) {
			if (direction == "L" || direction == "R") direction = "D";
		}
		else if (keyCode == KeyEvent.VK_LEFT) {
			if (direction == "U" || direction == "D") direction = "L";
		}
	}

	@Override
	public void keyReleased(KeyEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void keyTyped(KeyEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		if (isStarted && !isFailed) {
			moveSnake();
			
			if (snakex[0] == foodx && snakey[0] == foody) {
				len ++ ;
				score += 10;
				moveSnake();
				do {
					foodx = 25 + 25 * rand.nextInt(34);
					foody = 75 + 25 * rand.nextInt(20);
				} while (isFoodInSnake());
			}
			
			for (int i = 1; i < len; i ++ ) {
				if (snakex[i] == snakex[0] && snakey[i] == snakey[0]) {
					isFailed = true;
				}
			}
			
			repaint();
		}
		timer.start();
	}
}
