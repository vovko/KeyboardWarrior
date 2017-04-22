float x, y, radius;
 
int WIDTH = 900;
int HEIGHT = 300;
 
import java.util.Date;

String[] current_frame_lines; //= [];// = loadStrings("list.txt");
String[] previous_frame_lines;// = [];// = loadStrings("list.txt");

BufferedReader reader;
String line;
 
 
void setup() {
  surface.setSize(WIDTH, HEIGHT);
 
  background(100);
  smooth();
  frameRate(999999);
  
  
 reader = createReader("/home/vovko/PycharmProjects/KeyboardWarrior/keylogger/log/keys.log"); 
}
 
void draw_frame_counter() {
  int box_width = 60;
  int box_height = 18;
  int padding = 2;
 
  int localX = width - box_width - padding;
  int localY = padding;
 
  String frame_rate = int(frameRate) + " fps";
 
  color text_color = #00ff00;
 
  int box_centre_x = localX + (box_width/2);
  int box_centre_y = localY + (box_height/2) - padding;
 
  // Frame rate box
  fill(150, 150, 150);
  noStroke();
  rect(localX, localY, box_width, box_height);
 
  // Frame rate text
  fill(text_color);
  textAlign(CENTER, CENTER);
  text(frame_rate, box_centre_x, box_centre_y);
}
 
 
void draw() {
  fill(0);
 
  x = random(width);
  y = random(height);
  radius = random(200);
 
  //fill(random(255));
  //ellipse(x, y, radius, radius);
 
 
  fill(150, 150, 150);
  noStroke();
  rect(10, 10, 200, 100);
   
 
  //String path = sketchPath("/home/vovko/PycharmProjects/KeyboardWarrior/keylogger/log/keys.log");
  //File file = new File(path);
 
  fill(255, 255, 255);
 
  textAlign(LEFT, TOP);
  
  long last_modified =  123;// file.lastModified()
 
  text("last change: " + last_modified , 20 , 20);
  //Date millisec = new Date(file.lastModified());
  //println(millisec.getTime());
  draw_frame_counter();
  
  read_key_strokes(); 
  
}

void read_key_strokes() {
  
  
  String[] current_frame_lines = loadStrings("/home/vovko/PycharmProjects/KeyboardWarrior/keylogger/log/keys.log");
  //String[] previous_frame_lines;// = [];// = loadStrings("list.txt");
  println(current_frame_lines.length);

  //String[] lines = loadStrings("list.txt");
  //println("there are " + lines.length + " lines");
  //for (int i = 0 ; i < lines.length; i++) {
    //println(lines[i]);

  

}