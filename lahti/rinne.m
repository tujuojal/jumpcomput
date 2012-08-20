%this one is for forward stepping solver

function [a,v,s,t]=rinne(steps)
	%time steps size, 100seconds / how many steps
	dt=30/steps;
	%constants
	D=0.25;	%airresistance crossectional constant
	g=9.81;	%gravity
	m=80;	%average mass of rider
	C=0.055;	%friction coefficient
	A=D/m;	%airresistant coefficient
	%initialize with
	%zeros
	t=zeros(steps,1);
	s=zeros(steps,1);
	v=zeros(steps,1);
	a=zeros(steps,1);
	x=zeros(steps,1);
	y=zeros(steps,1);
	a(1)=sin(alpha(s(1)))*g-cos(alpha(s(1)))*g*C;
	
	%forward stepping solution with finite differences for speed  
	for (i=1:steps)
		t(i+1)=t(i)+dt;
		a(i+1)=sin(alpha(s(i)))*g-cos(alpha(s(i)))*sign(v(i))*g*C-sign(v(i))* v(i)^2*A;
		v(i+1)=max(dt*a(i+1)+v(i),0);
		s(i+1)=dt*v(i+1)+s(i);
		x(i+1)=x(i)+cos(alpha(s(i)))*(s(i+1)-s(i));
		y(i+1)=y(i)-sin(alpha(s(i)))*(s(i+1)-s(i));


		
	end
	plot(x,y);
	hold on;
	
	
	%etsitään jkoku tietty kohta lähtöpisteestä
	etsittava=80;
	piste=0;
	for (i=1:steps)
		if (s(i)>etsittava)
			piste=i;
			break;
		endif;
	end;
		
lento(30/360*pi*2,v(piste),x(piste),y(piste));	
v(piste)*3.6

%seuraava laskee rinteen kulman annetussa kohdassa (pituus rinteen pintaa pitkin)
function kulma=alpha(kohta)
	if (kohta<40)
		kulma=30/360*pi*2;
	elseif (kohta<60)
		kulma=(60-kohta)*30/20/360*pi*2;
		elseif(kohta<70) 
		kulma=0;
		elseif(kohta<80)
		kulma=(70-kohta)*30/10/360*pi*2;
		else
			kulma=0;
	endif
		
	%vakiofunktio näin aluksi
