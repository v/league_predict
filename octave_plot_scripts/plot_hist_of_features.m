D = csvread('../data/bayes.csv');

subplot(1, 2, 1);
hist(D(:,1),10);
hold on;
subplot(1, 2, 2);
hist(D(:,2),max(D(:,2)))

pause;
