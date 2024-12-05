
import React, { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
  const [primaryCategories, setPrimaryCategories] = useState([]);
  const [selectedPrimary, setSelectedPrimary] = useState(null);
  const [subcategories, setSubcategories] = useState([]);
  const [selectedOptions, setSelectedOptions] = useState({});
  const [captureCode, setCaptureCode] = useState("");

  useEffect(() => {
    axios.get("/api/primary_categories").then((response) => {
      setPrimaryCategories(response.data);
    });
  }, []);

  const handlePrimarySelect = (id, code) => {
    setSelectedPrimary({ id, code });
    setSubcategories([]);
    setSelectedOptions({});
    setCaptureCode("");
    axios.get(`/api/subcategories/${id}`).then((response) => {
      setSubcategories(response.data);
    });
  };

  const handleOptionChange = (subcategoryId, value, isMultiple) => {
    setSelectedOptions((prev) => {
      const updated = { ...prev };
      if (isMultiple) {
        updated[subcategoryId] = updated[subcategoryId] || [];
        if (updated[subcategoryId].includes(value)) {
          updated[subcategoryId] = updated[subcategoryId].filter((v) => v !== value);
        } else {
          updated[subcategoryId].push(value);
        }
      } else {
        updated[subcategoryId] = value;
      }
      return updated;
    });
  };

  const buildCaptureCode = () => {
    axios
      .post("/api/build_code", {
        primary_code: selectedPrimary.code,
        selections: selectedOptions,
      })
      .then((response) => {
        setCaptureCode(response.data.capture_code);
      });
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Lithology Capture Code Generator</h1>
      <div>
        <h2>Select Primary Category</h2>
        {primaryCategories.map((category) => (
          <button
            key={category.id}
            onClick={() => handlePrimarySelect(category.id, category.code)}
            style={{
              margin: "5px",
              padding: "10px",
              backgroundColor: selectedPrimary?.id === category.id ? "lightblue" : "white",
            }}
          >
            {category.name}
          </button>
        ))}
      </div>

      {subcategories.length > 0 && (
        <div>
          <h2>Select Subcategories</h2>
          {subcategories.map((subcategory) => (
            <div key={subcategory.id}>
              <h3>{subcategory.name}</h3>
              <div>
                {subcategory.single_choice ? (
                  <select
                    onChange={(e) =>
                      handleOptionChange(subcategory.id, e.target.value, false)
                    }
                  >
                    <option value="">--Select--</option>
                    {subcategory.options.map((option) => (
                      <option key={option.id} value={option.code}>
                        {option.name}
                      </option>
                    ))}
                  </select>
                ) : (
                  subcategory.options.map((option) => (
                    <label key={option.id} style={{ margin: "0 10px" }}>
                      <input
                        type="checkbox"
                        value={option.code}
                        onChange={() =>
                          handleOptionChange(subcategory.id, option.code, true)
                        }
                      />
                      {option.name}
                    </label>
                  ))
                )}
              </div>
            </div>
          ))}
          <button onClick={buildCaptureCode} style={{ marginTop: "20px" }}>
            Generate Capture Code
          </button>
        </div>
      )}

      {captureCode && (
        <div>
          <h2>Capture Code</h2>
          <p>{captureCode}</p>
        </div>
      )}
    </div>
  );
};

export default App;
