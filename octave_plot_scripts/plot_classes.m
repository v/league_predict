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

for i=1:10
    R2 = [];
    O2 = [];
    Y2 = [];
    B2 = [];
    for j=1:rows(R)
        if(R(j,7) == i)
            R2 = [R2;R(j,:)];
        end
    end
    for j=1:rows(O)
        if(O(j,7) == i)
            O2 = [O2;O(j,:)];
        end
    end
    for j=1:rows(Y)
        if(Y(j,7) == i)
            Y2 = [Y2;Y(j,:)];
        end
    end
    for j=1:rows(B)
        if(B(j,7) == i)
            B2 = [B2;B(j,:)];
        end
    end
    subplot(5, 2, i)
    scatter(R2(:,3),R2(:,2),'red');
    hold on;
    scatter(O2(:,3),O2(:,2),[],[.8 .6 0]);
    hold on;
    scatter(Y2(:,3),Y2(:,2),'yellow');
    hold on;
    scatter(B2(:,3),B2(:,2),'blue')
    hold on;
    if(i == 1 || i == 2)
        title('Difficulties from 1 to 10');
    end
    if(i == 9 || i == 10)
        xlabel('# Times Free') 
    end
    if(mod(i,2) == 1)
        ylabel('# Weeks Since Last Free')
    end
end

pause;
