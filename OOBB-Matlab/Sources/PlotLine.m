function [ linePlot ] = PlotLine( xs, ys, color, style, width )
%PLOTLINE Summary of this function goes here
%   Detailed explanation goes here

xlim = [-110, 110];

m = ( ys(2) - ys(1) ) / ( xs(2) - xs(1) );
n = ys(2) - xs(2) * m;

y1 = ( m * xlim(1) ) + n;
y2 = ( m * xlim(2) ) + n;

hold on

linePlot = line([xlim(1) xlim(2)], [y1 y2], ...
            'Color', color, ...
            'LineStyle', style, ...
            'LineWidth', width );

hold off
zoom on

end

