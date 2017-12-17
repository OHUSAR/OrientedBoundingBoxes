CURRENT_DIR = GetFileFolder( mfilename( 'fullpath' ) );
OBJ_DIR = [ CURRENT_DIR filesep 'Data' filesep 'Object1' ];
SLICES_DIR = [ OBJ_DIR filesep 'Slices' ];

COLORS = jet(8);

figure
axis equal;
title( 'Object Slicing Demo' );

objVertices = LoadVertices( [ OBJ_DIR filesep 'pts.txt' ] );
chVertices = LoadVertices( [ OBJ_DIR filesep 'ch.txt' ] );
oobbVertices = LoadVertices( [ OBJ_DIR filesep 'oobb.txt' ] );

chPlot = PlotObject( chVertices, COLORS(8,:), '-', 2 );
objPlot = PlotObject( objVertices, COLORS(1,:), '-', 1 );
oobbPlot = PlotObject( oobbVertices, COLORS(3,:), '-', 3 );

legend( [ objPlot(1), chPlot(1), oobbPlot(1) ],...
        'Original Object', 'Convex Hull', 'OOBB' );

X_LIMITS = get( gca, 'XLim' );
Y_LIMITS = get( gca, 'YLim' );

% ---- Slice 1
pause
     
axis1 = [ ( oobbVertices(1,:) + oobbVertices(2,:) ) * 0.5; ...
          ( oobbVertices(3,:) + oobbVertices(4,:) ) * 0.5 ];
axis1Plot = PlotLine( axis1(:,1), axis1(:,2), COLORS(4,:), '-.', 3 );

set(gca,'XLim', X_LIMITS);
set(gca, 'YLim', Y_LIMITS);

legend( [ objPlot(1), chPlot(1), oobbPlot(1), axis1Plot(1) ],...
        'Original Object', 'Convex Hull', 'OOBB', '1st slice axis' );
    
pause

set(objPlot, 'Visible', 'off' );
set(chPlot, 'Visible', 'off' );

sliceAv = LoadVertices( [ SLICES_DIR filesep 'sliceA.txt' ] );
sliceBv = LoadVertices( [ SLICES_DIR filesep 'sliceB.txt' ] );

sliceAPlot = PlotObject( sliceAv, COLORS(5,:), '-', 1 );
sliceBPlot = PlotObject( sliceBv, COLORS(6,:), '-', 1 );

legend( [ oobbPlot(1), axis1Plot(1), sliceAPlot, sliceBPlot ],...
         'OOBB', '1st slice axis', 'Slice A', 'Slice B' );

pause
% ---- Slice 2

axis2 = [ ( oobbVertices(2,:) + oobbVertices(3,:) ) * 0.5; ...
          ( oobbVertices(1,:) + oobbVertices(4,:) ) * 0.5 ];
axis2Plot = PlotLine( axis2(:,1), axis2(:,2), COLORS(4,:), '-.', 3 ); 

set(gca,'XLim', X_LIMITS);
set(gca, 'YLim', Y_LIMITS);

legend( [ oobbPlot(1), axis1Plot(1), sliceAPlot, sliceBPlot, axis2Plot ],...
         'OOBB', '1st slice axis', 'Slice A', 'Slice B', '2nd slice axis' );
     
pause

set(sliceAPlot, 'Visible', 'off' );
set(sliceBPlot, 'Visible', 'off' );

plots = cell(4);
for i = 1:4
   sliceV = LoadVertices( [ SLICES_DIR filesep 'slice' num2str(i-1) '.txt' ] );
   plots{i} = PlotObject( sliceV, COLORS(4+i,:), '-', 1 );
end

legend( [ oobbPlot(1), axis1Plot(1), axis2Plot, plots{1}, plots{2}, plots{3}, plots{4} ],...
         'OOBB', '1st slice axis', '2nd slice axis', 'Slice1', 'Slice2', 'Slice3', 'Slice4' );
     