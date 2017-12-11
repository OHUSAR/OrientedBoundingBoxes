points = 'pts.txt';
convexHull = 'ch.txt';
oobb = 'oobb.txt';

figure;
axis equal

oobbPlot = PlotObject( oobb, 'g', '-', 3 );
chPlot = PlotObject( convexHull, 'r', '-', 2 );
ptsPlot = PlotObject( points, 'b', '-', 1 );

legend( [ ptsPlot(1), chPlot(1), oobbPlot(1) ],...
        'Original Object', 'Convex Hull', 'OOBB' );