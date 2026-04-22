#!/usr/bin/env python3
"""
Deterministic Key Facts enricher for entity pages.

Walks wiki/entities/*.md and fills null/Unknown values in the Key Facts table
using deterministic heuristics from linked sources and frontmatter.
No LLM calls.
"""

import re
import yaml
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


def parse_entity_frontmatter(content: str) -> Optional[dict]:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return None
    
    end_idx = content.find('---', 3)
    if end_idx == -1:
        return None
    
    try:
        return yaml.safe_load(content[3:end_idx])
    except yaml.YAMLError:
        return None


def extract_key_facts_table(content: str) -> Optional[tuple[str, dict]]:
    """Extract Key Facts table from markdown. Returns (table_str, dict of facts)."""
    # Find Key Facts section
    match = re.search(r'\n## Key Facts\n\n(\|.*?\|.*?\n(?:\|.*?\n)*)', content, re.MULTILINE)
    if not match:
        return None
    
    table_str = match.group(1)
    facts = {}
    
    # Parse markdown table
    lines = table_str.strip().split('\n')
    for line in lines[2:]:  # Skip header and separator
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        if len(cells) == 2:
            field, value = cells
            facts[field] = value
    
    return (table_str, facts)


def find_linked_sources(entity_content: str, entity_name: str) -> list[str]:
    """Find source pages linked in entity body or that reference this entity."""
    wiki_root = Path('/home/jbl/projects/labs-wiki/wiki')
    sources_dir = wiki_root / 'sources'
    
    linked = []
    
    # Check for explicit wikilinks in entity body
    wikilinks = re.findall(r'\[\[([^\]]+)\]\]', entity_content)
    for link in wikilinks:
        if 'wiki/sources/' in link:
            slug = link.split('wiki/sources/')[-1]
            source_file = sources_dir / f'{slug}.md'
            if source_file.exists():
                linked.append(str(source_file))
    
    # Reverse-scan sources for references to this entity
    entity_slug = entity_name.lower().replace(' ', '-')
    for source_file in sources_dir.glob('*.md'):
        try:
            content = source_file.read_text('utf-8', errors='ignore')
            if entity_slug in content.lower() or entity_name in content:
                if str(source_file) not in linked:
                    linked.append(str(source_file))
        except:
            pass
    
    return linked


def extract_github_creator(url: str) -> Optional[str]:
    """Extract creator from github URL."""
    match = re.match(r'https://github\.com/([^/]+)/', url)
    return match.group(1) if match else None


def extract_arxiv_created(url: str) -> Optional[str]:
    """Extract created date from arxiv URL/ID."""
    # Extract arxiv ID
    match = re.search(r'(\d{4})\.(\d{5})', url)
    if not match:
        return None
    
    yymm = match.group(1)
    # Convert YYMM to YYYY-MM
    # 2509 -> 2025-09
    yy = int(yymm[:2])
    mm = int(yymm[2:])
    
    # Simple heuristic: if yy < 50, assume 20yy, else 19yy
    yyyy = 2000 + yy if yy < 50 else 1900 + yy
    
    return f'{yyyy:04d}-{mm:02d}'


def extract_arxiv_info_from_source(source_path: str, entity_name: str) -> dict:
    """Extract arxiv metadata from source content."""
    result = {}
    
    try:
        content = Path(source_path).read_text('utf-8', errors='ignore')
        
        # Try to extract created from arxiv ID in frontmatter or URL
        frontmatter = parse_entity_frontmatter(content)
        if frontmatter and 'source_url' in frontmatter:
            source_url = frontmatter['source_url']
            if 'arxiv.org' in source_url:
                created = extract_arxiv_created(source_url)
                if created:
                    result['Created'] = created
        
        # Extract first author from abstract or authors section
        author_match = re.search(
            r'\*\*Authors?:\*?\s*([^,\n]+)',
            content,
            re.IGNORECASE
        )
        if author_match:
            author = author_match.group(1).strip()
            # Take first author only
            if ',' in author:
                author = author.split(',')[0].strip()
            result['Creator'] = author
    except:
        pass
    
    return result


def extract_metadata_from_blog_source(source_path: str) -> dict:
    """Extract metadata from Google Research blog sources."""
    result = {}
    
    try:
        content = Path(source_path).read_text('utf-8', errors='ignore')
        
        # Check if it's a Google Research blog source
        frontmatter = parse_entity_frontmatter(content)
        if frontmatter:
            source_url = frontmatter.get('source_url', '')
            if 'research.google/blog' in source_url:
                result['Creator'] = 'Google Research'
    except:
        pass
    
    return result


def enrich_entity(entity_file: Path) -> dict:
    """Enrich a single entity file. Returns stats."""
    stats = {'entities_processed': 0, 'fields_filled': 0}
    
    try:
        content = entity_file.read_text('utf-8', errors='ignore')
    except:
        return stats
    
    # Parse frontmatter
    frontmatter = parse_entity_frontmatter(content)
    if not frontmatter:
        return stats
    
    # Extract key facts table
    extracted = extract_key_facts_table(content)
    if not extracted:
        return stats
    
    table_str, facts = extracted
    entity_name = frontmatter.get('title', entity_file.stem)
    sources = frontmatter.get('sources', [])
    
    stats['entities_processed'] = 1
    
    # Find linked sources
    linked_sources = find_linked_sources(content, entity_name)
    if not linked_sources and sources:
        linked_sources = [
            f'/home/jbl/projects/labs-wiki/{s}' if not s.startswith('/') else s
            for s in sources
        ]
    
    # Try to fill missing fields
    new_facts = facts.copy()
    
    for field in ['Type', 'Created', 'Creator', 'URL', 'Status']:
        if field not in new_facts or new_facts[field] in ['Unknown', 'N/A', '']:
            filled = False
            
            # Try source frontmatter
            for source_path in linked_sources:
                if not Path(source_path).exists():
                    continue
                
                try:
                    source_fm = parse_entity_frontmatter(
                        Path(source_path).read_text('utf-8', errors='ignore')
                    )
                    if not source_fm:
                        continue
                    
                    source_url = source_fm.get('source_url', '')
                    
                    if field == 'URL' and source_url:
                        # Check if entity slug appears in source URL
                        entity_slug = entity_name.lower().replace(' ', '-')
                        if entity_slug in source_url.lower():
                            new_facts[field] = source_url
                            stats['fields_filled'] += 1
                            filled = True
                            break
                        # Fallback: use source URL if entity seems related
                        if new_facts.get(field) in ['Unknown', 'N/A', '']:
                            new_facts[field] = source_url
                            stats['fields_filled'] += 1
                            filled = True
                    
                    if field == 'Created' and 'arxiv.org' in source_url:
                        created = extract_arxiv_created(source_url)
                        if created:
                            new_facts[field] = created
                            stats['fields_filled'] += 1
                            filled = True
                            break
                    
                    if field == 'Creator':
                        # Try GitHub
                        if 'github.com' in source_url:
                            creator = extract_github_creator(source_url)
                            if creator:
                                new_facts[field] = creator
                                stats['fields_filled'] += 1
                                filled = True
                                break
                        
                        # Try Google Research blog
                        if 'research.google/blog' in source_url:
                            new_facts[field] = 'Google Research'
                            stats['fields_filled'] += 1
                            filled = True
                            break
                        
                        # Try arxiv authors
                        if 'arxiv.org' in source_url:
                            arxiv_info = extract_arxiv_info_from_source(source_path, entity_name)
                            if 'Creator' in arxiv_info:
                                new_facts[field] = arxiv_info['Creator']
                                stats['fields_filled'] += 1
                                filled = True
                                break
                
                except:
                    pass
            
            if not filled and field == 'Status' and new_facts.get(field) in ['Unknown', 'N/A', '']:
                new_facts[field] = 'Active'
                stats['fields_filled'] += 1
    
    # Rebuild table if anything changed
    if new_facts != facts:
        header = '| Field | Value |\n|-------|-------|\n'
        rows = '\n'.join(f'| {k} | {v} |' for k, v in new_facts.items())
        new_table = header + rows
        
        content = content.replace(table_str, new_table)
        
        try:
            entity_file.write_text(content, 'utf-8')
        except:
            pass
    
    return stats


def main():
    """Enrich all entity files."""
    entities_dir = Path('/home/jbl/projects/labs-wiki/wiki/entities')
    
    total_entities = 0
    total_fields = 0
    
    for entity_file in sorted(entities_dir.glob('*.md')):
        stats = enrich_entity(entity_file)
        total_entities += stats['entities_processed']
        total_fields += stats['fields_filled']
    
    print(f'enriched {total_entities} entities, {total_fields} fields filled')
    return 0


if __name__ == '__main__':
    exit(main())
