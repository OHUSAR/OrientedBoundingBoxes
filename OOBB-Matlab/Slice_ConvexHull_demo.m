CURRENT_DIR = GetFileFolder( mfilename( 'fullpath' ) );
OBJ_DIR = [ CURRENT_DIR filesep 'Data' filesep 'Object1' ];
SLICES_DIR = [ OBJ_DIR filesep 'Slices' ];

figure
axis equal;
title( 'Slice Convex Hull demo' );

cmap = jet(8);

sliceColors = cmap(1:4,:);
chColors = cmap(4:end,:);

for i = 1:4
   sliceV = LoadVertices( [ SLICES_DIR filesep 'slice' num2str(i-1) '.txt' ] );
   chV = LoadVertices( [ SLICES_DIR filesep 'ch' num2str(i-1) '.txt' ] );
   
   plotSlice = PlotObject( sliceV, sliceColors(i,:), '-', 1 );
   pause
   plotCh = PlotObject( chV, chColors(i,:), '-', 3 );
   pause
   
   %clf;
    
end