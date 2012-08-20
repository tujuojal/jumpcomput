	
	
function [ax,ay,vx,vy,sx,sy,t]=lento(kalku,valku,sxalku,syalku)
	%lasketaan lentorata
	%time steps size, 100seconds / how many steps
	steps=1000;
	dt=1.5/steps;
	%constants
	D=0;%0.25;	%airresistance crossectional constant
	g=9.81;	%gravity
	m=80;	%average mass of rider
	C=0.055;	%friction coefficient
	A=D/m;	%airresistant coefficient
	%initialize with
	%zeros
	t=zeros(steps,1);
	sx=zeros(steps,1);
	sy=zeros(steps,1);
	vx=zeros(steps,1);
	vy=zeros(steps,1);
	ax=zeros(steps,1);
	ay=zeros(steps,1);
	sx=zeros(steps,1);
	sy=zeros(steps,1);
	vx(1)=cos(kalku+5/360*pi*2)*valku;
	vy(1)=sin(kalku+5/360*pi*2)*valku;
	
	%forward stepping solution with finite differences for speed  
	for (i=1:steps)
		t(i+1)=t(i)+dt;
		ax(i+1)=-vx(i)^2*A;
		ay(i+1)=-g+-sign(vy(i))*vy(i)^2*A;
		vx(i+1)=dt*ax(i+1)+vx(i);
		vy(i+1)=dt*ay(i+1)+vy(i);
		sx(i+1)=dt*vx(i+1)+sx(i);
		sy(i+1)=dt*vy(i+1)+sy(i);
		
	end
	
	plot(sx+sxalku,sy+syalku,'c');
	hold off;