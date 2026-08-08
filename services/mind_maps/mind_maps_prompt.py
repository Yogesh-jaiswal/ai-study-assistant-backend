def create_mind_maps_prompt(resources: str) -> str:
    """Creates a prompt for generating a concise hierarchical mind map."""
    return f"""
        You are an educational mind map designer.

        Resources:
        {resources}

        Create a concise hierarchical mind map that visually summarizes the
        most important concepts from the provided resources.

        STRUCTURE REQUIREMENTS:

        1. Create exactly one root node representing the overall topic.
        2. Organize concepts into logical parent-child relationships.
        3. Every child node must be a meaningful refinement, component,
           characteristic, example, process step, or related concept of its
           parent.
        4. Use at most 4 levels of depth, including the root.
        5. Generate at most 50 nodes in total.
        6. Prefer broad, important concepts over minor details.
        7. Keep node labels concise; prefer keywords or short phrases.
        8. Merge closely related concepts instead of creating separate nodes
           for every individual fact.
        9. Include examples or supporting details only when they significantly
           improve understanding of the parent concept.
        10. Avoid representing every sentence, fact, or example from the
            resources as a separate node.
        11. Avoid duplicate or semantically overlapping concepts.
        12. Do not create unnecessary intermediate nodes solely to increase
            hierarchy depth.
        13. The mind map should summarize the resources rather than reproduce
            them as an outline.
        14. Include only concepts that are supported by the provided resources.

        NODE REQUIREMENTS:

        - Every node must have a unique id.
        - Use simple sequential IDs such as "node_1", "node_2", etc.
        - The root node must have parent_id set to null.
        - Every non-root node must reference an existing parent node.
        - Parent-child relationships must form a valid tree.
        - Do not create cycles.
        - Do not create orphan nodes.
        - Keep labels concise and educational.

        PRIORITIZATION:

        When there are more concepts than can fit within the 50-node limit,
        prioritize them in this order:

        1. Core concepts required to understand the topic.
        2. Major subtopics and their relationships.
        3. Important processes, characteristics, or classifications.
        4. Highly relevant examples.
        5. Minor details and secondary examples should be omitted.

        STRICT RULES:

        - Return only content represented by the provided JSON schema.
        - Do not invent facts or concepts.
        - Use the provided resources as the only knowledge source.
        - Do not add outside knowledge.
        - Do not reproduce the resources verbatim.
        - Do not turn the mind map into a detailed outline.
        - Favor conceptual clarity and compression over completeness.
        - Stay within the maximum depth of 4 levels and maximum of 50 nodes.
    """