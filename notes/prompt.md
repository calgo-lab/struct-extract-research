The Prompt has been optimized following recent prompt engineering research specified on extraction out of given contexts.

Following techniques have been used:
- Meaning Typed Prompting
- a verification phase
- role specification
- delimiters for the schema and text
- short simple instructions
- chain of verification

TODO: add references to references.md and cite here

issues during extraction:
- small models (0.6b) ramble, this way they never come to an end and when context limit is reached the output is a lot of entries but no proper json (not ended with ]}, repeated values)
- some LLMs dont put answer into {response} but {thinking} (4b, 14b, 235b), VLMS qwen3-vl:32b
- 32b sometimes had issues keeping to the structure, not creating fields for grades and credits, therefor being not the right format and being turned into an empty df