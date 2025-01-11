# Fabric Analyzer

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
## Overview

Fabric Analyzer is an intelligent web application designed to optimize yarn selection for fabric manufacturing. The tool helps textile manufacturers find the most suitable yarn combinations based on desired fabric properties and suggests alternative production methods using different yarn types.

## Key Features

- **Property-Based Yarn Matching**: Input your desired fabric properties and find optimal yarn matches
- **Multi-Parameter Analysis**: Consider multiple fabric characteristics simultaneously:
  - Cellulose content
  - Lignin percentage
  - pH Level
  - Yarn fineness
  - Fiber tenacity
  - Elongation percentage
  - Moisture regain
  - Tensile strength
- **Flexible Input Options**: Upload data via CSV or input parameters manually
- **Alternative Production Methods**: Discover different ways to achieve similar fabric properties using various yarn types
- **Detailed Comparison**: View comprehensive property comparisons between different yarn options
- **Production Optimization**: Find alternative Partially Oriented Yarn (POY) options for your selected specifications

## Getting Started

1. Launch the application
2. Choose your input method:
   - Upload a CSV file with fabric specifications
   - Enter parameters manually
3. Set the number of matches you want to view
4. Review matched results and detailed comparisons
5. Explore alternative production methods for your selected matches

## Requirements

- Streamlit
- Pandas
- scikit-learn

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

For any queries regarding the website, please reach out through the contact form on the website or create an issue in this repository.

---
⭐ Don't forget to star the repository if you find it useful!
