function [V,Xn,Yn]=nokkaPlot2(beta,p)
%nokan x-pituus on aina 5m ja se on suora taso kulmassa beta
%oletus on etta vauhtia nokalla voidaan arvioida oletuksella etta suunnan
%muutos rinteesta nokalle ei syo vauhtia ~~aka kaari kulmaksi
%p on hyppyrin paikka, se kohta johon asti lasketaan rinteen pintaa pitkin

%v0 on vauti rinteen suuntaan
%X on nokan karjen X koord
%Y on nokan karjen y koord
[D,g,m,myy,alastulo,nokka,alfa,valku]=param;
v0=vauhtiPlot2(valku,p);
p=nokka/cos(beta);          %nokan pituus nokkaa pitkin
B=(+sin(beta)*g+cos(beta)*g*myy);    
A=1/m*D;
%etsitaan aika T jolloin ollaan hyppyrin karjessa p 
T=fzero(@(t) -1/2/A*log(1+tan(0*(B*A)^(1/2)-atan(A*v0/(B*A)^(1/2)))^2)+1/2/A*log(1+tan(t*(B*A)^(1/2)-atan(A*v0/(B*A)^(1/2)))^2)+p,1);
%lasketaan vauhti hyppyrin karjessa
V=-tan(T*(B*A)^(1/2)-atan(A*v0/(A*B)^(1/2)))*(A*B)^(1/2)/A
t=(0:0.1:T);
v=-tan(t.*(B*A)^(1/2)-atan(A*v0/(A*B)^(1/2)))*(A*B)^(1/2)/A;
paikka=-1/2/A*log(1+tan(0*(B*A)^(1/2)-atan(A*v0/(B*A)^(1/2)))^2)+1/2/A.*log(1+tan(t.*(B.*A)^(1/2)-atan(A.*v0/(B.*A)^(1/2))).^2);
%plot(t,paikka);
x=[0 nokka];
y=[0 tan(beta)*nokka];
Xn=nokka;
Yn=tan(beta)*nokka;
plot(x,y,'r');
