function [v,x,y]=rinne(p)
if (p<10)
    alfa=pi*2/360*20;
    x=sin(alfa)*p;
    y=cos(alfa)*p;
    v=vauhtiPlot2(0,p,5/360*2*pi);
elseif (p<30)
    alfa=pi*2/360*10;
    x=sin(pi*2/360*20)*10+sin(alfa)*(p-10);
    y=cos(pi*2/360*20)*10+cos(alfa)*(p-10);
    V1=vauhtiPlot2(0,10,5/360*2*pi);
    v=vauhtiPlot2(V1,p-10,10/360*2*pi);
else
    alfa=pi*2/360*20;
    x=sin(pi*2/360*20)*10+sin(alfa)*20+sin(pi*2/360*10)*(p-30);
    y=cos(pi*2/360*20)*10+cos(alfa)*20+cos(pi*2/360*10)*(p-30);
    V1=vauhtiPlot2(0,10,5/360*2*pi);
    V2=vauhtiPlot2(V1,20,10/360*2*pi);
    v=vauhtiPlot2(V2,p-30,5/360*2*pi);
end

