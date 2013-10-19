D = csvread('../data/kyle.csv');

R = [];
O = [];
Y = [];
B = [];

for i=1:rows(D)
    if(D(i,1) == 1)
        R = [R;D(i,:)];
    elseif(D(i,1) <= 5)
        O = [O;D(i,:)];
    elseif(D(i,1) <= 10)
        Y = [Y;D(i,:)];
    else
        B = [B;D(i,:)];
    end
end

scatter3(R(:,3),R(:,2),R(:,7),'red');
hold on;
scatter3(O(:,3),O(:,2),O(:,7),[],[.8 .6 0]);
hold on;
scatter3(Y(:,3),Y(:,2),Y(:,7),'yellow');
hold on;
scatter3(B(:,3),B(:,2),B(:,7),'blue')
title('Weeks Till Free (Red=1, Orange=2:5, Yellow=6:10, Blue=11..)')
xlabel('Number of Times Free') 
ylabel('Number of Weeks Since Last Free')
zlabel('Difficulty')

pause;
