"""MDX file parser for extracting frontmatter and components"""

import re
import yaml
from typing import Tuple, Optional, List


class MDXParser:
    """Parse MDX files and extract frontmatter"""

    @staticmethod
    def parse_frontmatter(content: str) -> Tuple[Optional[dict], str]:
        """Extract YAML frontmatter and content"""
        if not content.startswith('---'):
            return None, content

        # Find end of frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None, content

        try:
            frontmatter = yaml.safe_load(parts[1])
            content_body = parts[2]
            return frontmatter, content_body
        except yaml.YAMLError:
            return None, content

    @staticmethod
    def extract_components(content: str) -> List[Tuple[str, int]]:
        """Extract Mintlify components from MDX"""
        components = []

        # Match JSX-style components
        component_pattern = r'<(\w+)(?:\s+[^>]*)?>.*?</\1>|<(\w+)(?:\s+[^>]*)?/>'

        for match in re.finditer(component_pattern, content, re.DOTALL):
            component_name = match.group(1) or match.group(2)
            line_number = content[:match.start()].count('\n') + 1
            components.append((component_name, line_number))

        return components
