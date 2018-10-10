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
    n = 100;
   
    deltaI = del2(double(target));
    
    alpha = double(repmat(alpha,[1,1,3]));
    alpha = alpha./max(alpha(:));
    dst = double(src) .* alpha + deltaI .* (1-alpha);
    dst = uint8(dst);
    
    antDst = dst;
    
    for k = 1:n
        results = double(dst) .* (1-alpha);
        for i=1:size(dst,1)
            for j=1:size(dst,2)
                if results(i,j) ~= 0
                    if i > 10 && i < size(dst, 1) && j > 10 && j < size(dst, 2)
                        temp1 = antDst(i-10:i+10,j-10:j+10,:);
                        temp2 = uint8(zeros(21,21,3));
                        temp2(11,11,:) = antDst(i,j,:);
                        dst(i,j,:) = sum(sum(temp1-temp2))./440 + deltaI(i,j,:); 
                    %elseif i ==1 && j == 1   
                    end
                end
            end
        end
        antDst = dst;
    end
    
        
        
end

