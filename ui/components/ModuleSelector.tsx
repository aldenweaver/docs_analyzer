"use client";

import { useState } from "react";

export interface Module {
  id: string;
  name: string;
  description: string;
  category: string;
}

interface ModuleSelectorProps {
  title: string;
  modules: Module[];
  selectedModules: string[];
  onSelectionChange: (selected: string[]) => void;
}

export default function ModuleSelector({
  title,
  modules,
  selectedModules,
  onSelectionChange,
}: ModuleSelectorProps) {
  const categories = ["core", "high-impact", "advanced"];

  const handleSelectAll = () => {
    onSelectionChange(modules.map((m) => m.id));
  };

  const handleSelectNone = () => {
    onSelectionChange([]);
  };

  const handleToggle = (moduleId: string) => {
    if (selectedModules.includes(moduleId)) {
      onSelectionChange(selectedModules.filter((id) => id !== moduleId));
    } else {
      onSelectionChange([...selectedModules, moduleId]);
    }
  };

  const handleCategoryToggle = (category: string) => {
    const categoryModules = modules.filter((m) => m.category === category);
    const categoryModuleIds = categoryModules.map((m) => m.id);
    const allSelected = categoryModuleIds.every((id) => selectedModules.includes(id));

    if (allSelected) {
      // Deselect all in category
      onSelectionChange(
        selectedModules.filter((id) => !categoryModuleIds.includes(id))
      );
    } else {
      // Select all in category
      const newSelection = new Set([...selectedModules, ...categoryModuleIds]);
      onSelectionChange(Array.from(newSelection));
    }
  };

  const getCategoryModules = (category: string) => {
    return modules.filter((m) => m.category === category);
  };

  const isCategorySelected = (category: string) => {
    const categoryModules = getCategoryModules(category);
    return categoryModules.every((m) => selectedModules.includes(m.id));
  };

  const getCategoryName = (category: string) => {
    return category
      .split("-")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  return (
    <div className="bg-card rounded-lg border p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-semibold">{title}</h3>
        <div className="space-x-2">
          <button
            onClick={handleSelectAll}
            className="text-sm text-primary hover:underline"
          >
            Select All
          </button>
          <span className="text-muted-foreground">|</span>
          <button
            onClick={handleSelectNone}
            className="text-sm text-primary hover:underline"
          >
            Select None
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {categories.map((category) => {
          const categoryModules = getCategoryModules(category);
          if (categoryModules.length === 0) return null;

          return (
            <div key={category} className="space-y-2">
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id={`${title}-${category}`}
                  checked={isCategorySelected(category)}
                  onChange={() => handleCategoryToggle(category)}
                  className="w-4 h-4 rounded border-input cursor-pointer"
                />
                <label
                  htmlFor={`${title}-${category}`}
                  className="font-medium text-sm cursor-pointer"
                >
                  {getCategoryName(category)} ({categoryModules.length})
                </label>
              </div>

              <div className="ml-6 grid grid-cols-1 md:grid-cols-2 gap-2">
                {categoryModules.map((module) => (
                  <div key={module.id} className="flex items-start space-x-2">
                    <input
                      type="checkbox"
                      id={module.id}
                      checked={selectedModules.includes(module.id)}
                      onChange={() => handleToggle(module.id)}
                      className="w-4 h-4 mt-1 rounded border-input cursor-pointer"
                      data-testid={title.toLowerCase().includes('analyzer') ? 'analyzer-checkbox' : 'fixer-checkbox'}
                    />
                    <label
                      htmlFor={module.id}
                      className="text-sm cursor-pointer"
                    >
                      <div className="font-medium">{module.name}</div>
                      <div className="text-muted-foreground text-xs">
                        {module.description}
                      </div>
                    </label>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-4 text-sm text-muted-foreground">
        {selectedModules.length} of {modules.length} modules selected
      </div>
    </div>
  );
}
