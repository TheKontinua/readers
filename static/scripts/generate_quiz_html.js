// Accounts for images on the first line being indented.
// Without this, images may cause a horizontal scroll
// when the line width is 1.
const INDENT_FACTOR = .85;

/**
* Function to generate LaTeX into a new iframe using
* the given text and potential urls of the images to
* be put into the LaTeX.
*
* TODO: Allow the user to type the name of the
* image instead of the url (requires changing how
* files are uploaded to the server due to files
* being automaticly renamed when conflicts occur)
* @param {string} text 
* @param {array of type string} image_urls 
* @returns 
*/
function generate_latex(text, names, urls, box_width){
    let latex_wrapper = document.createElement("div");
    //let imageLineRatios = [];
    
    // Make generator with custom macros
    let generator = new latexjs.HtmlGenerator({
        CustomMacros: (function() {
        var args      = CustomMacros.args = {},
            prototype = CustomMacros.prototype;
      
        function CustomMacros(generator) {
            this.g = generator;
        }
          
        // Macro to allow the LaTeX to parse \textwidth without crashing
        // (does nothing)
        args['textwidth'] = ['H']
        prototype['textwidth'] = function() {
        }

        // Macro to add functionality for include graphics command
        // Supports setting width relative to textwidth
        args['includegraphics'] = ['H', 'o?', 'u'];

        // parameters of a LaTeX macro are distributed to the corresponding parameters
        // of the function defined here
        prototype['includegraphics'] = function(width, given_name) {
            let image = document.createElement("img");
            for(let i = 0; i < names.length; ++i){
                let raw_name = names[i].substring(0, names[i].lastIndexOf("."));
                if(given_name == raw_name){
                    image.src = (urls[i]);
                }
            }
            image.classList.add("latex_image");
            latex_wrapper.appendChild(image);

            if(width){
                // The actual string for the width parameter is stored in width.textContent
                width = width.textContent;
                width = width.replaceAll(" ", "");
                let width_split_equals = width.split("=");
                if(width_split_equals.length >= 1 && width_split_equals[0] === "width"){
                    image.setAttribute("data-width", width_split_equals + "");
                    let ratio = parseFloat(width_split_equals[1]);
                    let width = (Math.round(ratio * (box_width)) * INDENT_FACTOR)+ "";
                    image.width = width;
                }
            } else {
                image.setAttribute("data-line-width", 1);
                //imageLineRatios.push(1.0);
            }
            // return image in an array to add it to the LaTeX
            return [image];
          };
          return CustomMacros;
        }())
    });
    generator = latexjs.parse(text, { generator: generator });
    $('head').append(generator.stylesAndScripts('https://cdn.jsdelivr.net/npm/latex.js/dist/'));
    $('body').append(generator.domFragment());
}

/**
 * Calculates the width of an HTMLElement in pixels using the
 * BoundingClientRect. This method will fail if the HTMLElement
 * is not attached to the DOM.
 * @param {HTMLElement} htmlElement The element to get the width of. 
 * @returns The width of the HTMLElement in pixels.
 */
function widthHTMLElement(htmlElement){
    return htmlElement.offsetWidth;
}

/**
 * Resizes the images within the given iFrame containing 
 * LaTeX generated by the custom macro.
 * @param {HTMLIFrameElement} latexFrame The iframe containing images.
 */
function resizeIframe(latexFrame){
        if(latexFrame.contentDocument != null){
        let images = latexFrame.contentDocument.getElementsByClassName("latex_image");
        if(images != null){
        for(let i = 0; i < images.length; ++i){
            // The float value is stored after the comma in the attribute value
            let ratio = parseFloat(images.item(i).getAttribute('data-width').split(',')[1]);
            images.item(i).width = (Math.round(ratio * (widthHTMLElement(latexFrame.contentDocument.body))) * INDENT_FACTOR)+ "";
        }
    }
    }
}




/**
 * Initializes an iFrame containing an image from the custom macro.
 * This initialization gets rid of unneeded scrollbars, ensures
 * the iframe takes up the entire container and has images dynamicly
 * resized appropriately.
 * @param {HTMLIFrameElement} latexFrame The iframe to initialize.
 */
function initLatexFrame(latexFrame){
    // Max height to prevent scrollbar by default
    latexFrame.style.height="95%";
    latexFrame.style.width= "100%";
    latexFrame.style.padding = 0;
    latexFrame.contentDocument.height = "100%";
    latexFrame.contentDocument.width = "100%";
    resizeIframe(latexFrame);
    
    rs = new ResizeObserver((entries) => {
        for (const entry of entries) {
            resizeIframe(latexFrame);
        }});
    rs.observe(latexFrame);
}


/**
 * Make and return attribute label with a given name, associated
 * class and value
 * @param {string} name - The name of the label
 * @param {string} value_class - The class to associate with the label
 * @param {string} value - The value that the innerHTML the label should contain
 * @returns A p tag containing an attribute name and its value
 */
function make_attribute_label(name, value_class, value){
    var p = document.createElement("p");
    $(p).addClass("small_margin");

    var span_title = document.createElement("span");
    $(span_title).addClass("bold_font");
    span_title.innerHTML = name;

    var span_value = document.createElement("span");
    span_value.innerHTML = value;
    $(span_value).addClass(value_class)

    p.appendChild(span_title);
    p.appendChild(span_value);
    return p;
}


// helper function to display 1 question
function display_question(data, container, button_function, isQuizQuestion, isInitial, quiz_state){
    let list_item = document.createElement("li");
        list_item.id = data["question_id"];
                            
        // border for each question
        let border_wrapper = document.createElement("div");
        $(border_wrapper).addClass("bordered");
                        
        // wrapper containing question meta data
        let question_wrapper = document.createElement("div");
        question_wrapper.style.float = "left";
        $(question_wrapper).addClass("question_metadata");
        if(isQuizQuestion){
            if(isInitial)
                quiz_state.set(data["ordering"], data);
            question_wrapper.appendChild(make_attribute_label("Ordering: ", "question_ordering", data["ordering"]));
        }
        
        // add attribute labels
        question_wrapper.appendChild(make_attribute_label("Difficulty: ", "conceptual_difficulty", data["conceptual_difficulty"]));
        question_wrapper.appendChild(make_attribute_label("Volume: ", "volume", data["volume"]));
        question_wrapper.appendChild(make_attribute_label("Chapter: ", "chapter", data["chapter"]));
        question_wrapper.appendChild(make_attribute_label("Creator: ", "creator", data["creator"]));
        question_wrapper.appendChild(make_attribute_label("Point Value: ", "point_value", data["point_value"]));
        question_wrapper.appendChild(make_attribute_label("Time (minutes): ", "time_required_mins", data["time_required_mins"]));
        border_wrapper.appendChild(question_wrapper);

        // wrapper for buttons
        let button_wrapper = document.createElement("div");
        button_wrapper.style.float = "right";
        $(button_wrapper).addClass("quiz_display_button_wrapper");

        // add buttons using function
        button_function(button_wrapper);
        border_wrapper.appendChild(button_wrapper);

        // add LaTeX
        let latex_wrapper = document.createElement("iframe");
        latex_wrapper.src = "/latex_window/question/" + data["question_id"] + "/"+ 
                            "question" + "/" + widthHTMLElement(container) + "/" ;
        border_wrapper.appendChild(latex_wrapper);

        list_item.appendChild(border_wrapper);
        container.appendChild(list_item);
        initLatexFrame(latex_wrapper);
        latex_wrapper.contentWindow.addEventListener(
            "message",
            (event) => {
                border_wrapper.style.height= (200 + latex_wrapper.contentDocument.body.offsetHeight) + "px";
            }
          );
}


/**
 * Function to display quiz questions in a given container (no return value)
 * @param {Object} data[i] - A JavaScript object containing the data for the quiz questions to display
 * @param {Object} data[i] - A JavaScript object containing the data for a quiz question to display
 * @param {string} data[i].conceptual_difficulty - A string of the difficulty of this question
 * @param {string} data[i].volume - A string of the volume of this question
 * @param {string} data[i].chapter - A string of the chapter of this question
 * @param {string} data[i].creator - A string of the creator of this question
 * @param {string} data[i].point_value - A string of the point value of this question
 * @param {string} data[i].time_required_mins - A string of the time required in minutes of this question
 * @param {string} question_container_id - The html id of the container to display the quiz questions in
 * @param {function} button_function  - The function to add buttons to the right of the attributes 
 * (needs to have a parameter to accept the div to add the buttons to)
 * @param {string} data[i].ordering - A string of the ordering of this question (only required if areQuizQuestions)
 * @param {dict} data[i].quiz_state - A dictionary to map order (int) to data representing the order questions should be displayed in
 */
function redisplay_questions(question_container_id, button_function, quiz_state){
    let container = document.getElementById(question_container_id);
    container.innerHTML = "";
    for(let [key, data] of quiz_state){
        display_question(data, container, button_function, true, false, quiz_state)
    };
}

/**
 * Function to display quiz questions in a given container (no return value)
 * @param {Object} data[i] - A JavaScript object containing the data for the quiz questions to display
 * @param {Object} data[i] - A JavaScript object containing the data for a quiz question to display
 * @param {string} data[i].conceptual_difficulty - A string of the difficulty of this question
 * @param {string} data[i].volume - A string of the volume of this question
 * @param {string} data[i].chapter - A string of the chapter of this question
 * @param {string} data[i].creator - A string of the creator of this question
 * @param {string} data[i].point_value - A string of the point value of this question
 * @param {string} data[i].time_required_mins - A string of the time required in minutes of this question
 * @param {string} question_container_id - The html id of the container to display the quiz questions in
 * @param {function} button_function  - The function to add buttons to the right of the attributes 
 * (needs to have a parameter to accept the div to add the buttons to)
 * @param {boolean} areQuizQuestions - A boolean representing if this list are questions or quiz questions
 * (questions don't have ordering, but quiz questions do)
 * @param {string} data[i].ordering - A string of the ordering of this question (only required if areQuizQuestions)
 * @param {dict} data[i].quiz_state - An empty dictionary to map order (int) to data
 */
function display_questions(data, question_container_id, button_function, areQuizQuestions, quiz_state){
    let container = document.getElementById(question_container_id);
    container.innerHTML = "";
    for(const i in data){
        display_question(data[i], container, button_function, areQuizQuestions, true, quiz_state)
    };
}