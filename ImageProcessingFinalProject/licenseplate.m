I = imread('C:\Users\matthew.morais\Desktop\plateScene5.jpg');
if size(I,3)==3 % RGB image
  I=rgb2gray(I);
end

[r,c] = size(I);

figure
imshow(I);
%pause(5);

ed = edge(I,'Sobel');
ed = imdilate(ed,strel('square',5));
ed = bwareaopen(ed,500);
imshow(ed);
%pause(5);

propies = regionprops(ed,'BoundingBox');

allblobs = I;
for n=1:size(propies,1)
  x = propies(n).BoundingBox;
  % use aspect ratio of an american license plate to find it in the scene
  aspectRatio = x(3)/x(4);
  if aspectRatio > 1.75 && aspectRatio < 2
      disp(aspectRatio);
      plateLocationImage = insertShape(I,'rectangle',[x(1) x(2) x(3) x(4)]);
      bb = propies(n).BoundingBox;
  end
  allblobs = insertShape(allblobs,'rectangle',[x(1) x(2) x(3) x(4)]);
  allblobs = insertText(allblobs,[x(1) x(2)],string(aspectRatio));
end
figure
imshow(allblobs);
%pause(5);
Plate = imcrop(I,bb);
[matlab, mine] = plate2text(Plate);
disp(matlab);
disp(mine);

final_image = insertShape(I,'rectangle',[bb(1) bb(2) bb(3) bb(4)]);
final_image = insertText(final_image,[bb(1) bb(2)],"Plate");
final_image = insertText(final_image,[bb(1) bb(2)+bb(4)],matlab);
final_image = insertText(final_image,[bb(1)+bb(3) bb(2)+bb(4)],mine);
imshow(final_image);


%% F u n c t i o n s



function [Plate, Plate_mine] = plate2text(input_image)
    %%% Initialization
    I = input_image;
    I = imresize(I,[600,800]);

    % get letters and numbers for comparison
    letters = getLetters('C:\Users\matthew.morais\Pictures\Letters\');

    if size(I,3)==3 % RGB image
      I=rgb2gray(I);
    end
    test = histeq(I);
    %%% Process input image of license plate
    O = test > 100;

    % use this to ensure the letters are always white.
    if mean(mean(O)) > 0.5
        O = ~O;
    end


    [L, Ne]=bwlabel(O);

    % Measure properties of image regions
    propied = regionprops(O,'BoundingBox');

    % we know the size of the box should be roughly 1/3 the size of the
    % plate, so we can also filter on that
    ymin = size(O,1)/3;
    ymax = size(O,1)-ymin;
    % final output string
    Plate = [];
    Plate_mine = [];
    out = test;
    % loop through each object found in region props
    for n=1:size(propied,1)
      x = propied(n).BoundingBox;
      % use aspect ratio of box to find letters.. can assume box is roughly the
      % same for all license plates
      aspectRatio = x(3)/x(4);

      ypix = x(4);

      % check aspect ratio is roughly what we expect, and that the minimum y
      % requirement is met suggesting it is a letter.
      if aspectRatio < 0.40 && aspectRatio > 0.20 && ypix > ymin && ypix < ymax
        % rectangle('Position',propied(n).BoundingBox,'EdgeColor','g','LineWidth',2) % for plotting
        % get region for letter
        [r,c] = find(L==n);
        % give us a 5 pixel padding on each letter, in all directions
        n1=O(min(r)-5:max(r)+5,min(c)-5:max(c)+5);
        %imshow(~n1);
        % use build in matlab OCR
        n1 = imerode(imfill(edge(n1,'Sobel'),'holes'),strel('disk',2));
        imshow(n1);
        matlab_letter = matlabOCR(~n1);
        Plate = [Plate,matlab_letter];
        my_letter = myOCR(n1,letters);
        Plate_mine = [Plate_mine,my_letter];
        out = insertShape(out,'rectangle',[x(1) x(2) x(3) x(4)]);
        out = insertText(out,[x(1) x(2)],string(n));
        out = insertText(out,[x(1) x(2)+25],string(matlab_letter));
        out = insertText(out,[x(1) x(2)+50],string(my_letter));
      end
    end
    try
        Plate_mine = strjoin(Plate_mine,"");
    catch
        Plate_mine = "???";
        Plate = "???";
    end
    imshow(out);
    pause(5);
end

function output = matlabOCR(inputImage)
% Uses built in OCR, and a preset letter dictionary to determine characters
% ONLY.
    txt = ocr(inputImage,"TextLayout","character","CharacterSet","ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789");
    output = txt.Text;
end

function output = myOCR(inputImage,letters)
    % takes an input image, and checks what letter it most likely is 
    
    % convert struct to index.. this is the dictionary i read in using the
    % letters i hand drew in paint
    fns = fieldnames(letters);
    [sz,~] = size(fns);
    maxMatch = 0;
    for i = 1:sz
        letr = imresize(letters.(fns{i}),size(inputImage));
        match = sum(inputImage(:)==letr(:));
        msg = strcat((fns{i}),' - ',string(match));
        if match > maxMatch
            maxMatch = match;
            output = string((fns{i}));
        end
    end

    if output == 'one'
        output =1;
    elseif output == 'two'
        output = 2;
    elseif output =='three'
        output = 3;
    elseif output == 'four'
        output = 4;
    elseif output == 'five'
        output = 5;
    elseif output == 'six'
        output = 6;
    elseif output == 'seven'
        output = 7;
    elseif output == 'eight'
        output = 8;
    elseif output == 'nine'
        output = 9;
    end
    
end

function output = getLetters(directory)
    % loads letter dictionary for comparisons
    dirData = dir(directory);
    [row,~] = size(dirData);
    for i = 3:row
        % build full file directory
        file = strcat(dirData(i).folder,"\",dirData(i).name);
        % read the file
        I = imread(file);
        % convert to BW
        I = rgb2gray(I);
        % add image to struct
        output.(extractBetween(file,"Letters\",".png")) = ~I;
    end
        
end
