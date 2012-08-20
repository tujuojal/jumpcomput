function testi2ga

[x fval, exitflag,output]=ga(@lento2,2,[],[],[],[],[10*2*pi/360,50],[60*2*pi/360,500]);
lentoPlot2(x);
disp(x(1)/(2*pi)*360);
disp(x(2));
disp(-fval);
disp(output);