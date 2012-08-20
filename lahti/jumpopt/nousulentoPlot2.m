function [Tkorkein,V,X,Y,Xn,Yn]=nousulentoPlot2(beta,p)
%beta on nokan kulma
%v0 on nopeus nokan lopussa nokan suuntaan
%V on (x-suuntainen) nopeus lakipisteessa
%X on x-koord lakipisteessa
%Y on y-koord lakipisteessa
%Tkorkein on aika joka kestaa etta ollaan lakipisteessa
%p on paikka josta hyppyri alkaa

[v0,Xn,Yn]=nokkaPlot2(beta,p);
[D,g,m,myy,alastulo,nokka,alfa]=param;

vxa=cos(beta)*v0;
vya=sin(beta)*v0;

a=D/m;



%etsitaan se T jolloin vynousu=0 eli ollaan korkeimmalla
Tkorkein=fzero(@(t) -tan(t.*(g*a)^(1/2)-atan(a*vya/(g*a)^(1/2)))*(g*a)^(1/2)/a,1)
V=1./(a*Tkorkein+1/vxa)       %nopeus lakipisteessa

%paikka Y lakipisteessa
Y=-1/2/a*log(1+tan(Tkorkein*(g*a)^(1/2)-atan(a*vya/(g*a)^(1/2)))^2)+1/2/a*log(1+tan(0*(g*a)^(1/2)-atan(a*vya/(g*a)^(1/2)))^2)
%sama numeerisesti
quad(@(t) -tan(t*(g*a)^(1/2)-atan(a*vya/(g*a)^(1/2)))*(g*a)^(1/2)/a,0,Tkorkein)

%paikka X lakipisteessa
X=log(a*Tkorkein+1/vxa)/a-log(a*0+1/vxa)/a;
%sama numeerisesti
%quad(@(t) 1./(a*t+1/vxa),0,Tkorkein)

%kuvaajia tarkistamista varten
 

t=(0:.001:Tkorkein);
 x=log(a.*t+1./vxa)./a-log(a.*0+1./vxa)./a;
 ynousu=-1/2/a.*log(1+tan(t.*(g.*a).^(1/2)-atan(a.*vya./(g.*a).^(1/2))).^2)+1/2/a.*log(1+tan(0*(g*a)^(1/2)-atan(a*vya/(g*a)^(1/2)))^2);


 plot(x+Xn,ynousu+Yn);

