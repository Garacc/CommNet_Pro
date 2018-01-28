import java.awt.Color;  
import java.awt.FlowLayout;  
import java.awt.Graphics;  
import java.util.ArrayList;  
import java.util.Collections;  
import java.util.Comparator;  
import java.util.List;  
import java.util.Random;  
import javax.swing.JFrame;  
  
public class Aloha extends JFrame{  
    //站点基数为1  
    public static int base = 1;  
    //站点总数  
    public int MaxStation;  
    //时间段需要设置比较长，不然每个时间槽的冲突的可能很大，也就无法仿真了  
    public final int randTime = 1000;  
    //successPost越大，越接近真实情况，曲线也越清晰  
    private int successPost = 1000;  
    //时间槽大小  
    public final int time = 2;  
    //帧的总数  
    public int countPoint = 0;  
    //站队列  
    private List<Data> list;  
    //画布  
    private Graphics g;  
      
    //设置最大发送站点数  
    public void setNum(int num){  
        this.MaxStation = num;  
    }  
      
    //仿真函数  
    public void GetStatus() {  
        Random r = new Random();  
        int total = 0;  
        int success = 0;  
        list = new ArrayList<Data>();  
          
        //随机产生站点发送数据时间  
        for (int i = 0; i < MaxStation; i++) {  
            Data d = new Data(r.nextInt(randTime)+1);  
            list.add(d);  
        }  
          
        //发送时间排序  
        Comparator<Data> comparator = new Comparator<Data>() {  
            public int compare(Data d1, Data d2) {                    
                    return d1.time - d2.time;  
            }             
        };        
        Collections.sort(list,comparator);  
          
        int count = 0;          //记录经历过的时间周期  
        while(true){              
            int temcount = 0;   //记录每个时间槽发送帧的次数  
            for(int i = 0; i < MaxStation; i++){  
                if(list.get(i).time >= count * time && list.get(i).time <= (count+1)*time){  
                    total += 1;  
                    temcount += 1;  
                }else{  
                    break;  
                }  
            }  
            count++;  
            if(temcount == 0){  //没有帧  
                //continue;  
            }else if(temcount == 1){    //成功发送数据  
                success += 1;  
                list.get(0).set(r.nextInt(randTime)+1+count*time);  
                if(success > successPost){  
                    break;  
                }  
            }else if(temcount > 1){      //冲突，在随机产生发送数据时间  
                for(int j = 0; j < temcount; j++){  
                    list.get(j).set(r.nextInt(randTime)+1+count*time);  
                }  
            }  
            Collections.sort(list,comparator);  
        }  
        drawPoint((int)((1.0 * total/count)* 70 + 100), (int)(400-(10.0 * success/count)*29));  
//      System.out.println("每包时的尝试次数："+(1.0 * total/count));  
//      System.out.println("吞吐量："+(1.0*success/count));           
    }  
  
    public static void main(String[] args) {  
        Aloha aloha = new Aloha();  
        aloha.initUI();     //初始化UI  
        int i = 0;  
        while(true){  
            i++;  
            aloha.setNum(base*i);   //增加站点数  
            aloha.GetStatus();  
        }  
    }  
      
    public void paint(Graphics g){  
        super.paint(g);  
        draw(g);  
    }  
    //初始化界面  
    public void draw(Graphics g){  
        g.setColor(Color.RED);  
        g.drawLine(100, 400, 500, 400);  
        g.drawLine(100,100,100,400);  
        g.drawString("0", 90, 405);  
          
        for(int i = 1; i <= 5; i++){  
            g.drawString("|", 100+70*i, 398);  
            g.drawString(i+"", 100+70*i, 413);  
        }  
        g.drawString("G(每包时尝试次数)", 260,430);  
          
          
        for(int i = 1; i <= 10; i++){  
            g.drawString("-", 100 , 400-29*i);  
            if(i != 10){  
                g.drawString("0."+i, 80 , 400-29*i);  
            }else{  
                g.drawString(i/10+".0", 80 , 400-29*i);  
            }  
        }         
        int Stringx = 60;  
        int Stringy = 180;  
        g.drawString("每", Stringx, Stringy);  
        g.drawString("包", Stringx, Stringy+14);  
        g.drawString("时", Stringx, Stringy + 14*2);  
        g.drawString("的", Stringx, Stringy + 14*3);  
        g.drawString("吞", Stringx, Stringy + 14*4);  
        g.drawString("吐", Stringx, Stringy + 14*5);  
        g.drawString("量", Stringx, Stringy + 14*6);  
        g.drawString("S", Stringx, Stringy + 14*7+10);  
        g.setColor(Color.BLACK);  
    }  
      
    //话点  
    public void drawPoint(int x,int y){  
        g.drawLine(x, y, x, y);  
    }  
      
    //初始化界面参数  
    public void initUI(){  
        FlowLayout f1 = new FlowLayout();  
        this.setTitle("Aloha协议");  
        this.setLayout(f1);  
        this.setSize(640,480);  
        this.setResizable(false);  
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);  
        this.setVisible(true);  
        this.g = this.getGraphics();  
    }  
}  