# Pre-processor for NLP

[![Run on Ainize](https://ainize.ai/images/run_on_ainize_button.svg)](https://ainize.web.app/redirect?git_repo=https://github.com/fpem123/pre-processor)

This project pre-processor web server for NLP.

### Module requirement

    num2words
    waitress
    Unidecode
    contractions
    emoji
    flask


### How to use

    * First, Upload text file
    * Second, Select pre-processing option.
    * If the option requires an additional value, fill in the "value".
    * If the option requires an additional value, fill in the "value2".


### Pre-processing option

    space_normalizer: Whitespace normalization. (Including newline removal). No additional value required.

    emoji_remover: Remove emojis. No additional value required.

    html_tag_remover: Remove the html tag. No additional value required.

    url_remover: Remove url. No additional value required.

    word_replacer: Replace the word with another one you entered. Need additional value, value2.


### Post parameter

    text_file: Text file you want to pre-process. And only Text file.
    option: The pre-processing option.
    value: The value required by the specific option.
    value2: Second value required by specific option.

### Output foramt

    text/plain


## * With CLI *

### Input & Output example


Sample data download: [GitHub](https://github.com/fpem123/pre-processor/blob/master/data/test.txt)


#### Text_file
    
    Hello, guys my name is Kïm. And I have 10-blocks.
    I like         Orange🍊🍊🍊 & Banana🍌 @ peach🍑🍑 that yummy...!
    <hr>
    
    Okay; I love it. I can eat 23 oranges at same time.
    
    lol
    Oh.... you can't? sorry😢.


#### space_normalizer

* input: option=space_normalizer, value=whatever, value2=whatever


    curl -X POST "https://master-pre-processor-fpem123.endpoint.ainize.ai/dpp" -H "accept: text/plain" -H "Content-Type: multipart/form-data" -F "option=space_normalizer" -F "value=" -F "value2=" -F "text_file=@sample.txt;type=text/plain"

* output


    Hello, guys my name is Kïm. And I have 10-blocks. I like Orange🍊🍊🍊 & Banana🍌 @ peach🍑🍑 that yummy...! <hr> Okay; I love it. I can eat 23 oranges at same time. lol Oh.... you can't? sorry😢. 


#### emoji_remover

* input: option=emoji_remover, value=whatever, value2=whatever


    curl -X POST "https://master-pre-processor-fpem123.endpoint.ainize.ai/dpp" -H "accept: text/plain" -H "Content-Type: multipart/form-data" -F "option=emoji_remover" -F "value=" -F "value2=" -F "text_file=@sample.txt;type=text/plain"

* output


    Hello, guys my name is Km. And I have 10-blocks.
    I like         Orange & Banana @ peach that yummy...!
    <hr>
    
    Okay; I love it. I can eat 23 oranges at same time.
    
    lol
    Oh.... you can't? sorry.


#### html_tag_remover

* input: option=html_tag_remover, value=whatever, value2=whatever

    
    curl -X POST "https://master-pre-processor-fpem123.endpoint.ainize.ai/dpp" -H "accept: text/plain" -H "Content-Type: multipart/form-data" -F "option=html_tag_remover" -F "value=" -F "value2=" -F "text_file=@sample.txt;type=text/plain"


* output: 


    Hello, guys my name is Kïm. And I have 10-blocks.
    I like         Orange🍊🍊🍊 & Banana🍌 @ peach🍑🍑 that yummy...!
    
    
    Okay; I love it. I can eat 23 oranges at same time.
    
    lol
    Oh.... you can't? sorry😢.


#### word_replacer

* input: option=word_replacer, value=Orange, value2=Apple



    curl -X POST "https://master-pre-processor-fpem123.endpoint.ainize.ai/dpp" -H "accept: text/plain" -H "Content-Type: multipart/form-data" -F "option=word_replacer" -F "value=Orange" -F "value2=Apple" -F "text_file=@sample.txt;type=text/plain"


* output



    Hello, guys my name is Kïm. And I have 10-blocks.
    I like         Apple🍊🍊🍊 & Banana🍌 @ peach🍑🍑 that yummy...!
    <hr>
    
    Okay; I love it. I can eat 23 oranges at same time.
    
    lol
    Oh.... you can't? sorry😢.


#### You can send multi option

* input: option=html_tag_remover, value=whatever, value2=whatever, option=space_normalizer, value=whatever, value2=whatever


    curl -X POST "https://master-pre-processor-fpem123.endpoint.ainize.ai/dpp" -H "accept: text/plain" -H "Content-Type: multipart/form-data" -F "option=special_replacer" -F "value=&@;" -F "value2=and" -F "option=html_tag_remover" -F "value=" -F "value2=" -F "option=space_normalizer" -F "value=" -F "value2=" -F "text_file=@sample.txt;type=text/plain"

    
* output


    Hello, guys my name is Kïm. And I have 10-blocks. I like Orange🍊🍊🍊 & Banana🍌 @ peach🍑🍑 that yummy...! Okay; I love it. I can eat 23 oranges at same time. lol Oh.... you can't? sorry😢.
    

## * With swagger *

API page: [In Ainize](https://ainize.ai/fpem123/pre-processor?branch=master)

## * With a Demo *

Demo page: [End-point](https://master-pre-processor-fpem123.endpoint.ainize.ai/)
