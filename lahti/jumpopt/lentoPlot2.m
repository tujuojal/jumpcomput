function Tkoko=lentoPlot2(arvot)
%alfa on rinteen kulma
%beta on nokan kulma
%v0 on nokan suuntainen nopeus nokan lopussa
%vxa on vaakanopeus huippukohdassa
%X on x paikka lennon korkeimmassa kohdassa)
%Y on y paikka lennon korkeimmassa kohdassa)
%Xn ja Yn on nokan koordinaatit
beta=arvot(1);
p=arvot(2);
[Tkorkein,vxa,X,Y,Xn,Yn]=nousulentoPlot2(beta,p);
[D,g,m,myy,alastulo,nokka,alfa]=param;

vya=0;
a=D/m;

       %korkeus nokalta alastuloon
%zy ja vy on negatiivisia
%funktiot zy,zx paikka koordinaatti ajanhetk. t vx,vy nopeuskomp. hetk. t
%vy=tanh(-t.*(g*a)^(1/2)+atanh(a*vya/(g*a)^(1/2)))*(g*a)^(1/2)/a;
%vx=1./(a.*t+1/vxa);
%hold on;
%fplot(@(t) tanh(-t*(g*a)^(1/2)+atanh(a*vya/(g*a)^(1/2)))*(g*a)^(1/2)/a,[0 20]);
%plot(t,vy,'--rs');

%------------------------------
%------------------------------
%%%% korvataan seuraava jollain fiksummalla, niin että voidaan muutta rinteen geometriaa
%------------------------------
%
%etsitaan se T jolla tullaan alastulon korkeudelle
%nokka+vx/sqrt(vx^2+vy^2)*(alastulo)+zx-1/tan(alfa)*(tan(beta)*nokka+zy+vy/sqrt(vx^2+
%vy^2)*(alastulo))=0
T=fzero(@(t)nokka+vx(t,vxa)/sqrt(vx(t,vxa)^2+vy(t,vxa)^2)*(alastulo)+zx(t,vxa)+X-1/tan(alfa)*(-tan(beta)*nokka-zy(t,vxa)-Y-vy(t,vxa)/sqrt(vx(t,vxa)^2+vy(t,vxa)^2)*(alastulo)),1)
t=(0:.01:T);
y=Y+1/2/a*log(tanh(t.*(g*a)^(1/2)-atanh(a*vya/(g*a)^(1/2)))-1)+1/2/a*log(tanh(t.*(g*a)^(1/2)-atanh(a*vya/(g*a)^(1/2)))+1)-(1/2/a*log(-a*vya/(g*a)^(1/2)-1)+1/2/a*log(-a*vya/(g*a)^(1/2)+1));

%paikka x,y integroimalla nopeuksia vx, vy
%alastuloon asti
XA=log(a*T+1/vxa)/a-log(a*0+1/vxa)/a+X;     %integroitu vx=1./(a.*t+1/vxa) valilla 0-T
quad(@(s) 1./(a.*s+1/vxa),0,T)+X;
YA=Y+1/2/a*log(tanh(T*(g*a)^(1/2)-atanh(a*vya/(g*a)^(1/2)))-1)+1/2/a*log(tanh(T*(g*a)^(1/2)-atanh(a*vya/(g*a)^(1/2)))+1)-(1/2/a*log(-a*vya/(g*a)^(1/2)-1)+1/2/a*log(-a*vya/(g*a)^(1/2)+1));
x=log(a.*t+1/vxa)/a-log(a*0+1/vxa)/a+X;
plot(x+Xn,y+Yn,'g');
Tkoko=-(T+Tkorkein);

%plotataan alastulo
alastulox=[XA,XA+vx(T,vxa)/sqrt(vx(T,vxa)^2+vy(T,vxa)^2)*(alastulo)];
alastuloy=[YA,YA+vy(T,vxa)/sqrt(vx(T,vxa)^2+vy(T,vxa)^2)*(alastulo)];
plot(alastulox+Xn,alastuloy+Yn,'r');
%lasketaan alastulon lumimäärä
alstulolumi=(alastulox(1)-alastulox(2))*(alastuloy(2)-alastuloy(1))/2
%laatikon lumi, ilman nokan korkeutta
laatiklumi=(-alastulox(1))*alastuloy(1)
%nokan lumi
nokanlumi=tan(beta)*Xn*Xn/2
%leveys 30m lasketaan kokolumi
kokolumi=30*(nokanlumi+alstulolumi+laatiklumi)
%alastulon kulma
alskulma=atan2(alastuloy(1)-alastuloy(2),alastulox(2)-alastulox(1))/2/pi*360

function zy=zy(t,vxa)
D=0.25;
g=9.81;
m=80;
vya=0;
a=D/m;
zy=1/2/a*log(tanh(t*(g*a)^(1/2)-atanh(a*vya/(g*a)^(1/2)))-1)+1/2/a*log(tanh(t*(g*a)^(1/2)-atanh(a*vya/(g*a)^(1/2)))+1)-(1/2/a*log(tanh(0*(g*a)^(1/2)-atanh(a*vya/(g*a)^(1/2)))-1)+1/2/a*log(tanh(0*(g*a)^(1/2)-atanh(a*vya/(g*a)^(1/2)))+1));

function zx=zx(t,vxa)
D=0.25;
g=9.81;
m=80;
vya=0;
a=D/m;
zx=log(a*t+1/vxa)/a-log(a*0+1/vxa)/a;

function vy=vy(t,vxa)
D=0.25;
g=9.81;
m=80;
vya=0;
a=D/m;
vy=tanh(-t*(g*a)^(1/2)+atanh(a*vya/(g*a)^(1/2)))*(g*a)^(1/2)/a;

function vx=vx(t,vxa)
D=0.25;
g=9.81;
m=80;
vya=0;
a=D/m;
vx=1/(a*t+1/vxa);
