algoritimo 1

n=20 %definir o numero de lados 
theta = 2*pi/n %definir o angulo de rotacao 
mrot = [cos(theta), -sin(theta); sin(theta), cos(theta)]; %matriz de rotacao
v = zeros(2,n); %matriz dos vetores
v(:,1)= [1; 0]; %primeiro vetor
for i=2:n
    v(:,i)=mrot*v(:,i-1);
end

%desenho
axis equal;
grid on;
vp = [v v(:,1)];
plot(vp(1,:),vp(2,:))
title(sprintf('Polígono Regular de %d lados', n));
xlabel('Coordenada X');
ylabel('Coordenada Y');


algoritimo 2
%-a

n=5 %definir o numero de lados 
theta = 2*pi/n %definir o angulo de rotacao 
mrot = [cos(theta), -sin(theta); sin(theta), cos(theta)]; %matriz de rotacao
v = zeros(2,n); %matriz dos vetores
v(:,1)= [1; 0]; %primeiro vetor
for i=2:n
    v(:,i)=mrot*v(:,i-1);
end

%desenho
axis equal;
grid on;
vp = [v v(:,1)];
plot(vp(1,:),vp(2,:))
title(sprintf('Polígono Regular de %d lados', n));
xlabel('Coordenada X');
ylabel('Coordenada Y');



B

%angulo de 45 graus 
n=5 %definir o numero de lados 
theta = 2*pi/n %definir o angulo de rotacao 
mrot = [cos(theta), -sin(theta); sin(theta), cos(theta)]; %matriz de rotacao
v = zeros(2,n); %matriz dos vetores
v(:,1)= [1; 0]; %primeiro vetor
for i=2:n
    v(:,i)=mrot*v(:,i-1);
end

vt = [cos(pi/4 + pi/2); sin(pi/4 + pi/2)];

nt = 5;

for j = 1:nt
    v = v + vt; % Adiciona o vetor de translação na direção 45° com a horizontal
    vp = [v v(:,1)]; % Concatena o primeiro vetor ao final para fechar o polígono
    plot(vp(1,:),vp(2,:)); % Plota o polígono
    hold on;
end
axis equal;
grid on;
title(sprintf('Translacao'));
xlabel('Coordenada X');
ylabel('Coordenada Y');


C
% Número de lados do polígono
n = 5;

% Ângulo de rotação para os lados do polígono
theta = 2*pi/n;
mrot = [cos(theta), -sin(theta); sin(theta), cos(theta)]; % Matriz de rotação

% Vetores dos lados do polígono
v = zeros(2, n);
v(:,1) = [1; 0]; % Primeiro vetor
for i = 2:n
    v(:,i) = mrot * v(:,i-1); % Calcula os vetores dos lados
end

% Ângulo de rotação para a translação
ra = 30;
mr = [cosd(ra), -sind(ra); sind(ra), cosd(ra)]; % Matriz de rotação para a translação
vt = [cos(pi/4 + pi/2); sin(pi/4 + pi/2)]; % Vetor de translação

nt = 5; % Número de translações

for j = 1:nt
    for i = 1:n
        v(:,i) = mr * v(:,i); % Aplica a rotação em cada lado do polígono
    end
    
    v = v + vt; % Aplica a translação
    
    vp = [v v(:,1)]; % Concatena o primeiro vetor ao final para fechar o polígono
    plot(vp(1,:),vp(2,:)); % Plota o polígono
    hold on;
end

axis equal;
grid on;
title(sprintf('Polígono com rotação de 30° e translações'));
xlabel('Coordenada X');
ylabel('Coordenada Y');


D
% Número de lados do polígono
n = 7;
l = 2;

%cord inicias
xi = 5;
yi = 5;

% Ângulo de rotação para os lados do polígono
theta = 2*pi/n;
mrot = [cos(theta), -sin(theta); sin(theta), cos(theta)]; % Matriz de rotação

% Vetores dos lados do polígono
v = zeros(2, n);
v(:,1) = [l; 0]; % Primeiro vetor
for i = 2:n
    v(:,i) = mrot * v(:,i-1); % Calcula os vetores dos lados
end

v(1,:) = v(1,:) + x_init;
v(2,:) = v(2,:) + y_init;
vp = [v v(:,1)];
plot(vp(1,:),vp(2,:));


axis equal;
grid on;
title(sprintf('===================='));
xlabel('Coordenada X');
ylabel('Coordenada Y');



E
% número de lados do polígono
n = 7;

% Definição do raio da circunferência
rai = 2;

% Definição das velocidades angulares
o1 = pi/50; % Velocidade angular para girar em torno da origem
o2 = -pi/100; % Velocidade angular para girar em torno do centro do polígono

% Inicialização do ângulo de rotação em torno da origem e do centro do polígono
theta_O = 0;
theta_C = 0;

% Criação da figura
figure;
axis([-3 3 -3 3]);
axis equal;
grid on;

% Loop de animação
while true
    % Cálculo dos vetores dos lados do polígono
    theta_O = theta_O + o1; 
    theta_C = theta_C + o2; 
    
    % Cálculo dos vértices do polígono em torno da origem
    vo = zeros(2, n);
    for i = 1:n
        vo(:,i) = [rai * cos(theta_O + 2*pi*(i-1)/n); rai * sin(theta_O + 2*pi*(i-1)/n)];
    end
    
    % Cálculo do centro do polígono
    c = mean(vo, 2);
    
    % Translação dos vértices para o centro do polígono
    vC = vo - c;
    
    % Rotação dos vértices em torno do centro do polígono
    R = [cos(theta_C), -sin(theta_C); sin(theta_C), cos(theta_C)];
    vR = R * vC;
    
    % Translação de volta para a posição original
    v = vR + c;
    
    % Plotagem do polígono
    plot([v(1,:) v(1,1)], [v(2,:) v(2,1)], 'b');
    title('===================================');
    xlabel('Coordenada X');
    ylabel('Coordenada Y');
    grid on;
    axis([-3 3 -3 3]);
    axis equal;
    drawnow;
end

