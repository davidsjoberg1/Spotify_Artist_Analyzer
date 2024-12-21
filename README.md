# Spotify Artist Analyzer

Hello and welcome to my project. The inspiration for the project comes from [this video](https://www.youtube.com/watch?v=JheGL6uSF-4&t=348s) which analyzes the links between wikipedia pages. The purpose is for me to learn and explore and data can be collected, analyzed and visualized. In this README I will explain what I have done, and what I will do in the project. As I am still in an early stage I have not yet included a tutorial on how to use the code, but this might be added in the future. 

This project consist of downloading artist data, using the Spotify Web API, and find links between the artists. The Spotify Web API give me information about an artist like how many followers the artist have, how popular they are and what artists are related to them. To get data from as many artists as possible to do my analysis I have started with one artist and requested its related artists. For all the related artists I have done the same thing which makes the database of artists expand fast. Because of limitations in the request rate from the Spotify Web API it is taking time to gather this data, as Spotify has about 11 million aritsts. 

As of November 27th 2024 I have not been able to collect more artist data. This is becase a limitation that Spotify has set on its Web API, where apps in development mode can no more make requests for related artists, [link here](https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api). I have by this date gathered data of about 3 million artists, which is what I will use to make my analysis. 

For the analysis, I will use Python and C++. The functionality will be the same between the languages. The reason for this, is part because I want to improve my skills in both languages, but also because it can be interesting to analyze the differences between the performance of them.

The functionality that I will/have programmed is the following:
* [Find the path lenghts from artists to every other artist](#find-the-path-lenghts-from-artists-to-every-other-artist)
* [Community Detection](#community-detection)
* [Data Visualization](#data-visualization)

This list might get longer with time


## Find the path lenghts from artists to every other artist

Text to be updated.. but here is a video 
<iframe width="560" height="315" src="https://youtu.be/Q3XC9idfRwA" frameborder="0" allowfullscreen></iframe>(https://github.com/user-attachments/assets/cdf439fc-460b-4fa6-8312-f28eeb4683ca)

Just like in the Wikipedia graph video, I want to see what the longest paths are between artists. Since it is not time feasible to find the paths from every artist to every other artist in the database I will probably do this for about 10 000 artists, which should give me good enough data.
The code for the search is done through a bfs algoritm. I have done this in Python ([search_methods.py](data_analysis/search_methods.py))but not yet in C++. 

## Community Detection
I will do some kind of community detecion of the artists. I have not yet decided on what data I will base this on, but it will probably be on genres or popularity. I will probably use the Leiden Algoritm for the community detection. 

## Data Visualization
I will create some kind of graph to visialize the data, based on the community detection.









