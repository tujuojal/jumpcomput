function V=nokka2(beta,p)
%nokan x-pituus on aina nokka m ja se on suora taso kulmassa beta
%oletus on etta vauhtia nokalla voidaan arvioida oletuksella etta suunnan
%muutos rinteesta nokalle ei syo vauhtia ~~aka kaari kulmaksi
%p on hyppyrin paikka, se kohta johon asti lasketaan rinteen pintaa pitkin

%v0 on vauti rinteen suuntaan
[D,g,m,myy,alastulo,nokka,alfa,valku]=param;
v0=vauhti2(valku,p);
p=nokka/cos(beta);          %nokan pituus nokkaa pitkin
B=(+sin(beta)*g+cos(beta)*g*myy);    
A=1/m*D;
%etsitaan aika T jolloin ollaan hyppyrin karjessa p 
[T,fval,exitflag,output]=fzero(@(t) -1/2/A*log(1+tan(0*(B*A)^(1/2)-atan(A*v0/(B*A)^(1/2)))^2)+1/2/A*log(1+tan(t*(B*A)^(1/2)-atan(A*v0/(B*A)^(1/2)))^2)+p,1);
if(isnan(T)) %jos ei vauhti riita karkeen asti asetetaan lentovauhdiksi nolla
    V=0;

%lasketaan vauhti hyppyrin karjessa
else
    %disp(output);
V=-tan(T*(B*A)^(1/2)-atan(A*v0/(A*B)^(1/2)))*(A*B)^(1/2)/A;
t=(0:0.1:T);
v=-tan(t.*(B*A)^(1/2)-atan(A*v0/(A*B)^(1/2)))*(A*B)^(1/2)/A;
paikka=-1/2/A*log(1+tan(0*(B*A)^(1/2)-atan(A*v0/(B*A)^(1/2)))^2)+1/2/A.*log(1+tan(t.*(B.*A)^(1/2)-atan(A.*v0/(B.*A)^(1/2))).^2);
%plot(t,paikka);
end
