fname = '/Users/juangonzalezaguayo/Downloads/School/I2I - 2/Code/temp_data.txt';

file = strcat(fname);
temp = readtable(fname);
temp_1 = temp;

y = temp.Var1(:);
for row = 1: size(y)
    temp.Var2(row) = row;
end
x = temp.Var2(:);

figure(1);
plot(x, y)
title('Temperature vs Time')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')