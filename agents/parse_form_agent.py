import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from output_parsers import form_parser

load_dotenv()

page_source = """
    <!DOCTYPE html>
<html lang="en" class="h-100">

<head>
  <title>Web form</title>

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <link href="//cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <script src="//code.jquery.com/jquery-3.6.0.min.js"></script>
  <script src="//cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.bundle.min.js"></script>
  <script src="//unpkg.com/bootstrap-datepicker@1.9.0/dist/js/bootstrap-datepicker.min.js"></script>
  <link href="//unpkg.com/bootstrap-datepicker@1.9.0/dist/css/bootstrap-datepicker3.min.css" rel="stylesheet">
</head>

<body class="d-flex flex-column h-100">
  <main class="flex-shrink-2">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <h1 class="display-6">Web form</h1>
        </div>
      </div>
      <form method="get" action="submitted-form.html">
        <div class="row">
          <div class="col-md-4 py-2">
            <label class="form-label w-100">Text input
              <input type="text" class="form-control" name="my-text" id="my-text-id" myprop="myvalue">
            </label>

            <label class="form-label w-100">Password
              <input type="password" class="form-control" name="my-password" autocomplete="off">
            </label>

            <label class="form-label w-100">Textarea
              <textarea class="form-control" name="my-textarea" rows="3"></textarea>
            </label>

            <label class="form-label w-100">Disabled input
              <input class="form-control" type="text" name="my-disabled" placeholder="Disabled input" disabled>
            </label>

            <label class="form-label w-100">Readonly input
              <input class="form-control" type="text" name="my-readonly" value="Readonly input" readonly>
            </label>

            <div class="form-group tp-align-right mt-3">
              <a href="./index.html">
                Return to index
              </a>
            </div>
          </div>

          <div class="col-md-4 py-2">
            <label class="form-label w-100">Dropdown (select)
              <select class="form-select" name="my-select">
                <option selected>Open this select menu</option>
                <option value="1">One</option>
                <option value="2">Two</option>
                <option value="3">Three</option>
              </select>
            </label>

            <label class="form-label w-100">Dropdown (datalist)
              <input class="form-control" list="my-options" name="my-datalist" placeholder="Type to search...">
              <datalist id="my-options">
                <option value="San Francisco">
                <option value="New York">
                <option value="Seattle">
                <option value="Los Angeles">
                <option value="Chicago">
              </datalist>
            </label>

            <label class="form-label w-100">File input
              <input class="form-control" type="file" name="my-file">
            </label>

            <div class="form-check">
              <label class="form-check-label w-100">
                <input class="form-check-input" type="checkbox" name="my-check" id="my-check-1" checked>
                Checked checkbox
              </label>

              <label class="form-check-label w-100">
                <input class="form-check-input" type="checkbox" name="my-check" id="my-check-2">
                Default checkbox
              </label>
            </div>

            <div class="form-check">
              <label class="form-check-label w-100">
                <input class="form-check-input" type="radio" name="my-radio" id="my-radio-1" checked>
                Checked radio
              </label>
            </div>
            <div class="form-check">
              <label class="form-check-label w-100">
                <input class="form-check-input" type="radio" name="my-radio" id="my-radio-2">
                Default radio
              </label>
            </div>

            <button type="submit" class="btn btn-outline-primary mt-3">Submit</button>

          </div>

          <div class="col-md-4 py-2">
            <label class="form-label w-100">Color picker
              <input type="color" class="form-control form-control-color" name="my-colors" value="#563d7c">
            </label>

            <label class="form-label w-100">Date picker
              <input type="text" class="form-control" name="my-date">
            </label>

            <label class="form-label w-100">Example range
              <input type="range" class="form-range" name="my-range" min="0" max="10" step="1" value="5">
            </label>

            <input type="hidden" name="my-hidden">
          </div>
        </div>
      </form>
    </div>
  </main>
  <script>
    $('[name=my-date]').datepicker({
    });
  </script>
</body>

</html>
"""

# Parses the form and returns the list of objects
# describing the data to fill in the page
def parse_form_agent(page_source: str):
    llm = ChatOpenAI(
            temperature=0,
            model_name='gpt-4o-mini',
            api_key=os.environ["OPENAI_API_KEY"]
    )
    template = """Given the full page source {page_source}. It is a page for job application. It contains a form. I want you to parse it and return a list of json objects which will help identify all input fields required in the form. It will be used to fill the form using selenium. I want three things from you.
        1. Id: which will uniquely identify the tag
        2. Type: the type of id you found that I will pass in selenium
        3. Desc: Description of the data required by that field in my job application
    If you don't think there is an application form in this page then return an empty list.\n{format_instructions}
    """

    prompt_template = PromptTemplate(
        template= template, 
        input_variables=["page_source"],
        partial_variables={
            "format_instructions": form_parser.get_format_instructions()
        }
    )

    chain = prompt_template | llm | form_parser

    res = chain.invoke({'page_source': page_source})
    print(res)

if __name__=="__main__":
    parse_form_agent(page_source)
