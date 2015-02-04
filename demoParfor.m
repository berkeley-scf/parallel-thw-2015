nCores = 4;
mypool = parpool(nCores); 
% parpool open local nCores # alternative

n = 3000
nIts = 500
c = zeros(n, nIts);
parfor i = 1:nIts
     c(:,i) = eig(rand(n)); 
end

delete(mypool) 
% delete(gcp) works if you forget to name your pool by assigning the 
% output of parpool to a variable

