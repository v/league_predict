D = csvread('../data/free_features.csv');

sample_size = 16886;

%Number of weeks since free catagories: 0,1,2,3,4,5,6,7,8-10,11-13,13+

%c is count of occurance
c = zeros(10, 11);

%For each difficulty
for i=1:10
    %for each (number of weeks since free) catagory
    for j=0:7
        for k=1:rows(D)
            if(D(k,1) == i && D(k,2) == j)
                c(i,j + 1)++;
            end
        end
    end
    %catagory 8-10
    for k=1:rows(D)
        if(D(k,1) == i && D(k,2) >= 8 && D(k,2) <= 10)
            c(i,9)++;
        end
    end
    %catagory 11-13
    for k=1:rows(D)
        if(D(k,1) == i && D(k,2) >= 11 && D(k,2) <= 13)
            c(i,10)++;
        end
    end
    %catagory 13+
    for k=1:rows(D)
        if(D(k,1) == i && D(k,2) > 13)
            c(i,11)++;
        end
    end
end

c
prior = sum(sum(c)) / sample_size;
c / sample_size
disp(sprintf('P(free_next_week)=%f', prior));
for i=1:10
    for j=1:11
        disp(sprintf('P(free_next_week|difficulty=%d and catagory=%d)=%f', i, j, c(i,j) / sample_size));
    end
end
