import cm6  from "../dist/cm6.bundle.min.";

// Wrap all definition in a check for the presence of Shiny. This allows the JS
// to be loaded outside without causing errors.
if (Shiny) {
  class SQLEditorOutputBinding extends Shiny.OutputBinding {
    /**
     * Find the element that will be rendered by this output binding.
     * @param {HTMLElement} scope The scope in which to search for the element.
     * @returns {HTMLElement} The element that will be rendered by this output
     * binding.
     */
    find(scope) {
      return scope.find(".shiny-sql-editor");
    }

    /**
     * Function to run when rendering the output. This function will be passed
     * the element that was found by `find()` and the payload that was sent by
     * the server when there's new data to render. Note that the element passed
     * may already be populated with content from a previous render and it is up
     * to the function to clear the element and re-render the content.
     * @param {HTMLElement} el The element that was found by `find()`
     * @param {Record<String, Any>} payload An object with the following properties as provided by
     * `@render_tabulator:
     * - `columns`: An array of strings containing the column names
     * - `data`: An array of arrays containing the data
     * - `type_hints`: An array of objects containing the column types. Each
     *   object
     */
    renderValue(el, payload) {
      const view = cm6.createEditorView(undefined, el);
      const initialState = cm6.createEditorState("SELECT 42;");
      view.setState(initialState);
    
    }
  }
  Shiny.outputBindings.register(
    new SQLEditorOutputBinding(),
    "shiny-sql-editor"
  );
}