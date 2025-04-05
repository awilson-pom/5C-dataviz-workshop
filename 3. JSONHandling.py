#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import pandas as pd
from pandas import json_normalize

def print_section(title):
    """Helper function to print formatted section titles"""
    print(f"\n{'='*80}\n{title}\n{'='*80}")


# In[ ]:


# Part 1: Simple JSON Structure
print_section("Part 1: Simple JSON Structure")

# Create a simple JSON object
simple_json = {
    "students": [
        {"name": "Alice", "age": 20, "major": "CS"},
        {"name": "Bob", "age": 22, "major": "Math"},
        {"name": "Charlie", "age": 21, "major": "Physics"}
    ]
}

# Print the original JSON
print("\nOriginal JSON structure:")
print(json.dumps(simple_json, indent=2))

# Convert to DataFrame directly
print("\nMethod 1: Direct conversion to DataFrame")
df1 = pd.DataFrame(simple_json['students'])
print(df1)

# Using json_normalize
print("\nMethod 2: Using json_normalize")
df2 = json_normalize(simple_json['students'])
print(df2)


# In[ ]:


# Part 2: Nested JSON Structure
print_section("Part 2: Nested JSON Structure")

# Create a nested JSON object
nested_json = {
    "university": {
        "name": "Tech University",
        "departments": [
            {
                "name": "Computer Science",
                "students": [
                    {
                        "name": "Alice",
                        "grades": {"python": 95, "java": 88}
                    },
                    {
                        "name": "Bob",
                        "grades": {"python": 92, "java": 90}
                    }
                ]
            },
            {
                "name": "Mathematics",
                "students": [
                    {
                        "name": "Charlie",
                        "grades": {"calculus": 94, "statistics": 85}
                    }
                ]
            }
        ]
    }
}

print("\nNested JSON structure:")
print(json.dumps(nested_json, indent=2))

# Basic flattening
print("\nMethod 1: Basic flattening of departments")
df3 = json_normalize(nested_json['university']['departments'])
print(df3)

# Advanced flattening with meta data
print("\nMethod 2: Flattening with department info")
df4 = json_normalize(
    nested_json['university']['departments'],
    'students',
    ['name'],
    meta_prefix='department_',
    record_prefix='student_'
)
print(df4)


# In[ ]:


# Part 3: Practical Example
print_section("Part 3: Practical Example - Course Submissions")

# Create a practical example JSON
course_data = {
    "course": {
        "id": "CS101",
        "title": "Introduction to Programming",
        "assignments": [
            {
                "week": 1,
                "submissions": [
                    {"student": "Alice", "score": 95, "status": "submitted"},
                    {"student": "Bob", "score": 88, "status": "submitted"}
                ]
            },
            {
                "week": 2,
                "submissions": [
                    {"student": "Alice", "score": 92, "status": "submitted"},
                    {"student": "Bob", "score": None, "status": "missing"}
                ]
            }
        ]
    }
}

print("\nCourse data structure:")
print(json.dumps(course_data, indent=2))

# Flatten the course data
print("\nFlattened course data:")
df5 = json_normalize(
    course_data['course']['assignments'],
    'submissions',
    ['week']
)
print(df5)


# In[ ]:


# Create a pivot table
print("\nPivot table of scores by student and week:")
pivot_df = df5.pivot(columns='week', values='score', index='student')
pivot_df.columns = [f'Week_{col}' for col in pivot_df.columns]
print(pivot_df)


# In[ ]:




