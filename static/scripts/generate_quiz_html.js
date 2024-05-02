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
function generate_latex(text, image_urls){
    let latex_wrapper = document.createElement("iframe");
    let imageLineRatio = 1.0;

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
        prototype['includegraphics'] = function(width, given_url) {
            let image = document.createElement("img");
            image.src = given_url;
            image.id = "image";
            latex_wrapper.appendChild(image);

            if(width){
                // The actual string for the width parameter is stored in width.textContent
                width = width.textContent;
                width = width.replaceAll(" ", "");
                let width_split_equals = width.split("=");
                if(width_split_equals.length >= 1 && width_split_equals[0] === "width"){
                    imageLineRatio = parseFloat(width_split_equals[1]);
                }
            }
            // return image in an array to add it to the LaTeX
            return [image];
          };
          return CustomMacros;
        }())
    });
    generator = latexjs.parse(text, { generator: generator });
    
    // Generate htmlCode by looking for LaTeX.js files in the given directory    
    let htmlCode = generator.htmlDocument("https://cdn.jsdelivr.net/npm/latex.js/dist/");
    let srcdoc = htmlCode.head.outerHTML + htmlCode.body.outerHTML;
    latex_wrapper.srcdoc = srcdoc;

    function resize(){
        if(latex_wrapper.contentWindow){
            // TODO get elements by class, iterate through
            let image = latex_wrapper.contentWindow.document.getElementById("image");
            if(image){
                image.width = Math.round(imageLineRatio * (latex_wrapper.getBoundingClientRect().right - latex_wrapper.getBoundingClientRect().left)) + "";
            }
            latex_wrapper.style.height = (latex_wrapper.contentWindow.document.body.scrollHeight + 10) + 'px';
        }
    }
    
    latex_wrapper.onload = function(){
        resize();
    }

    latex_wrapper.onresize  = function(){
        resize();
    }

    latex_wrapper.height = "fit-content";
    latex_wrapper.width = "100%";
    
    return latex_wrapper;
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
 */
function display_questions(data, question_container_id, button_function, areQuizQuestions){
    let container = document.getElementById(question_container_id);
    container.innerHTML = "";
    for(const i in data){
        let list_item = document.createElement("li");
        list_item.id = data[i]["question_id"];
                            
        // border for each question
        let border_wrapper = document.createElement("div");
        $(border_wrapper).addClass("bordered");
                        
        // wrapper containing question meta data
        let question_wrapper = document.createElement("div");
        question_wrapper.style.float = "left";
        if(areQuizQuestions){
            question_wrapper.appendChild(make_attribute_label("Ordering: ", "question_ordering", data[i]["ordering"]));
        }
        
        // add attribute labels
        question_wrapper.appendChild(make_attribute_label("Difficulty: ", "conceptual_difficulty", data[i]["conceptual_difficulty"]));
        question_wrapper.appendChild(make_attribute_label("Volume: ", "volume", data[i]["volume"]));
        question_wrapper.appendChild(make_attribute_label("Chapter: ", "chapter", data[i]["chapter"]));
        question_wrapper.appendChild(make_attribute_label("Creator: ", "creator", data[i]["creator"]));
        question_wrapper.appendChild(make_attribute_label("Point Value: ", "point_value", data[i]["point_value"]));
        question_wrapper.appendChild(make_attribute_label("Time (minutes): ", "time_required_mins", data[i]["time_required_mins"]));
        border_wrapper.appendChild(question_wrapper);

        // wrapper for buttons
        let button_wrapper = document.createElement("div");
        button_wrapper.style.float = "right";
        $(button_wrapper).addClass("quiz_display_button_wrapper");

        // add buttons using function
        button_function(button_wrapper);
        border_wrapper.appendChild(button_wrapper);

        // add LaTeX
        let latex_wrapper = generate_latex(data[i]["question_latex"], data[i]["attachment_urls"]);
        border_wrapper.appendChild(latex_wrapper);

        list_item.appendChild(border_wrapper);
        container.appendChild(list_item);
    };
}