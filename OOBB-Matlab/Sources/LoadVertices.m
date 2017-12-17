function [ vertices ] = LoadVertices( filename )
%LOADVERTICES Summary of this function goes here
%   Detailed explanation goes here

vertices = load( filename );
vertices(end+1, : ) = vertices(1,:);

end

