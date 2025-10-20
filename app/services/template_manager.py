"""
Template manager for saving and loading evaluation criteria templates.
"""
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TemplateManager:
    """Manages criteria templates for reuse."""

    def __init__(self, storage_path: str = "data/templates.json"):
        """
        Initialize template manager.

        Args:
            storage_path: Path to JSON file for storing templates
        """
        self.storage_path = storage_path
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Create storage directory and file if they don't exist."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump({"templates": []}, f)

    def save_template(
        self,
        name: str,
        domain: str,
        criteria: List[Dict[str, Any]],
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Save a criteria template.

        Args:
            name: Template name
            domain: Domain (legal, medical, finance, general)
            criteria: List of criteria objects
            description: Optional description

        Returns:
            Saved template with ID and metadata
        """
        # Load existing templates
        templates = self._load_templates()

        # Generate ID
        template_id = f"tpl_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create template object
        template = {
            "id": template_id,
            "name": name,
            "domain": domain,
            "description": description or f"{name} criteria for {domain} domain",
            "criteria": criteria,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        # Add to templates
        templates.append(template)

        # Save
        self._save_templates(templates)

        logger.info(f"Saved template: {name} (ID: {template_id})")
        return template

    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific template by ID.

        Args:
            template_id: Template ID

        Returns:
            Template object or None if not found
        """
        templates = self._load_templates()

        for template in templates:
            if template["id"] == template_id:
                return template

        return None

    def list_templates(
        self,
        domain: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List all templates, optionally filtered by domain.

        Args:
            domain: Optional domain filter

        Returns:
            List of templates
        """
        templates = self._load_templates()

        if domain:
            templates = [t for t in templates if t["domain"] == domain]

        # Sort by created_at (newest first)
        templates.sort(key=lambda t: t["created_at"], reverse=True)

        return templates

    def update_template(
        self,
        template_id: str,
        name: Optional[str] = None,
        domain: Optional[str] = None,
        criteria: Optional[List[Dict[str, Any]]] = None,
        description: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Update an existing template.

        Args:
            template_id: Template ID
            name: New name (optional)
            domain: New domain (optional)
            criteria: New criteria (optional)
            description: New description (optional)

        Returns:
            Updated template or None if not found
        """
        templates = self._load_templates()

        for i, template in enumerate(templates):
            if template["id"] == template_id:
                # Update fields
                if name:
                    template["name"] = name
                if domain:
                    template["domain"] = domain
                if criteria:
                    template["criteria"] = criteria
                if description:
                    template["description"] = description

                template["updated_at"] = datetime.now().isoformat()

                templates[i] = template
                self._save_templates(templates)

                logger.info(f"Updated template: {template_id}")
                return template

        return None

    def delete_template(self, template_id: str) -> bool:
        """
        Delete a template.

        Args:
            template_id: Template ID

        Returns:
            True if deleted, False if not found
        """
        templates = self._load_templates()

        for i, template in enumerate(templates):
            if template["id"] == template_id:
                templates.pop(i)
                self._save_templates(templates)
                logger.info(f"Deleted template: {template_id}")
                return True

        return False

    def _load_templates(self) -> List[Dict[str, Any]]:
        """Load templates from storage."""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                return data.get("templates", [])
        except Exception as e:
            logger.error(f"Error loading templates: {e}")
            return []

    def _save_templates(self, templates: List[Dict[str, Any]]):
        """Save templates to storage."""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump({"templates": templates}, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving templates: {e}")
            raise


# Global instance
template_manager = TemplateManager()
