CURRENT_DIR = GetFileFolder( mfilename( 'fullpath' ) );
OBJ_DIR = [ CURRENT_DIR filesep 'Data' filesep 'Object1' ];

figure
axis equal;
title( 'Object Oriented Bouding Box Demo' );

objVertices = LoadVertices( [ OBJ_DIR filesep 'pts.txt' ] );
chVertices = LoadVertices( [ OBJ_DIR filesep 'ch.txt' ] );
oobbVertices = LoadVertices( [ OBJ_DIR filesep 'oobb.txt' ] );

chPlot = PlotObject( chVertices, 'r', '-', 2 );
objPlot = PlotObject( objVertices, 'b', '-', 1 );

BOXES_DIR = [ OBJ_DIR filesep 'Boxes' ];
boxes = dir( BOXES_DIR );

for boxFile = boxes'
    if ( boxFile.name(1) ~= '.' )
        candVertices = LoadVertices( boxFile.name );
        candidate = PlotObject( candVertices, 'g', '--', 1 );
        
        legend( [ objPlot(1), chPlot(1), candidate(1) ],...
        'Original Object', 'Convex Hull', 'OOBB candidate' );
        
        pause
        %set( candidate, 'Visible', 'off' );
    end
end

oobbPlot = PlotObject( oobbVertices, 'y', '-', 3 );

legend( [ objPlot(1), chPlot(1), oobbPlot(1) ],...
        'Original Object', 'Convex Hull', 'OOBB' );