function testi2ps

[x fval, exitflag,output]=patternsearch(@lento2,[10/360*2*pi,200],[],[],[],[],[10*2*pi/360,50],[60*2*pi/360,500]);
lentoPlot2(x);
disp(x(1)/(2*pi)*360);
disp(x(2));
disp(-fval);
disp(output);