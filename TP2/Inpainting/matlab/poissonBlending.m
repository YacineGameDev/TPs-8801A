function [ dst ] = poissonBlending( src, target, alpha )
%POISSONBLENDING Effectue un collage avec la méthode de Poisson
%   Remplit la zone de 'src' où 'alpha'=0 avec le laplacien de 'target'

    % Le problème de Poisson s'énonce par :
    % 'le laplacien de src est égal à celui de target là où alpha=0'
    % Pour résoudre ce problème, on utilise la méthode de Jacobi :
    % à chaque itération, un pixel est égal à la moyenne de ses voisins +
    % la valeur du laplacien cible
    
    % TODO Question 2 :
    
    %nombre d'iterations
    n = 1000;
   
    deltaIR = del2(double(target(:,:,1)));
    deltaIG = del2(double(target(:,:,2)));
    deltaIB = del2(double(target(:,:,3)));
    
    deltaI = zeros(size(target, 1),size(target, 2),3);
    deltaI(:,:,1) = deltaIR;
    deltaI(:,:,2) = deltaIG;
    deltaI(:,:,3) = deltaIB;
    deltaI = deltaI * 4;
    
    alpha = double(repmat(alpha,[1,1,3]));
    alpha = alpha./max(alpha(:));
    dst = double(src) .* alpha;
    dst = uint8(dst);
    
    for k = 1:n
        for i=1:size(dst,1)
            for j=1:size(dst,2)
                if alpha(i,j, :) ~= ones(1, 1, 3)
                        dst(i,j,:) = uint8((double(dst(i-1,j,:)) + double(dst(i+1,j,:)) ...
                                     + double(dst(i,j-1,:)) + double(dst(i,j+1,:)) + deltaI(i,j,:))./4);   
                end
            end
        end
    end  
        
end

