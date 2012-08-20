function V=vauhtiPlot2(v0,p)
[D,g,m,myy,alastulo,nokka,alfa]=param;
                                  
B=(sin(alfa)*g-cos(alfa)*g*myy);    
A=1/m*D;

%pitaisi etsia se t jolla ollaan tietyssa paikassa p
%(kuljettu matka p metria rinteen pintaa pitkin)? 
T=fzero(@(t) real((-1/2/A*log(tanh(t*(B*A)^(1/2)+atanh(A*v0/(B*A)^(1/2)))-1)-1/2/A*log(tanh(t*(B*A)^(1/2)+atanh(A*v0/(B*A)^(1/2)))+1)-(-1/2/A*log(tanh(0*(B*A)^(1/2)+atanh(A*v0/(B*A)^(1/2)))-1)-1/2/A*log(tanh(0*(B*A)^(1/2)+atanh(A*v0/(B*A)^(1/2)))+1))-p)),10)   %integroitu v=tanh(t*(B*A)^(1/2)+atanh(A*a/(B*A)^(1/2)))*(B*A)^(1/2)/A



t=(0:1:T+T);
v=real(tanh(t.*(B*A)^(1/2)+atanh(A*v0/(A*B)^(1/2)))*(A*B)^(1/2)/A);       %V ratkaistu dv/dt=B-A*v^2
V=real(tanh(T*(B*A)^(1/2)+atanh(A*v0/(A*B)^(1/2)))*(A*B)^(1/2)/A);

hold on;
grid on;
axis([-.5*p p -.5*p p]);

p=real((-1/2/A*log(tanh(t.*(B*A)^(1/2)+atanh(A*v0/(B*A)^(1/2)))-1)-1/2/A*log(tanh(t.*(B*A)^(1/2)+atanh(A*v0/(B*A)^(1/2)))+1)-(-1/2/A*log(tanh(0*(B*A)^(1/2)+atanh(A*v0/(B*A)^(1/2)))-1)-1/2/A*log(tanh(0*(B*A)^(1/2)+atanh(A*v0/(B*A)^(1/2)))+1))-p));
x=p*cos(alfa);
y=-p*sin(alfa);
%plot(t,p);
plot(x,y,'c');
