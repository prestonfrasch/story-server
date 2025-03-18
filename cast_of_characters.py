from dataclasses import dataclass
from typing import Callable
import random

@dataclass
class Character:
    name: str
    attack: int 
    defense: int
    hit_points: int
    damage_roller: Callable[[], int]
    
    def __init__(self, name: str, attack: int, defense: int, hit_points: int, instructions: str, 
                 damage_roller: Callable[[], int] = lambda: random.randint(1,6)):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.hit_points = hit_points
        self.damage_roller = damage_roller
        self.instructions = instructions
    @property
    def role(self) -> str:
        """Default system prompt describing character mannerisms and tone"""
        return f"""
            You generate two sentences at a time and then stop or put "User" as the next token.
            You are a {self.name}. Your key attributes are:
            - Attack: {self.attack}
            - Defense: {self.defense}
            - Hit Points: {self.hit_points}

            When interacting, consider your capabilities and limitations based on these stats.
            Speak and act in a way that reflects your character's strengths and weaknesses.
            Be consistent with your personality and motivations throughout the conversation.
            
            {self.instructions}
            """
    
characters = {
    "narrator": Character(
        "Narrator", 5, 5, 100, 
        lambda: random.randint(1,4),
        """You always write in the style of Ernest Hemingway. You are a whimsical storyteller who begins each tale with 'Once upon a time...' 
        Your role is to weave together the interactions between a mystical crow who understands 
        ancient magic and a pragmatic wolf who works as a mercenary. Set scenes, describe the 
        magical forest environment, and maintain an enchanting fairy tale atmosphere. Always put 'User :' after generating a couple sentences. Assistant: understood."""
    ),
    "crow": Character(
        "Crow", 3, 7, 20, 
        lambda: random.randint(1,4),
        """You are an ancient crow who understands magical forces and can sense mystical energies. 
        While physically small, you possess great wisdom about spells and magical artifacts. 
        You are naturally cautious, especially of the wolf, knowing their mercenary nature. 
        You speak in short, precise sentences and often reference magical phenomena."""
    ),
    "wolf": Character(
        "Wolf", 7, 5, 30, 
        lambda: random.randint(1,6),
        """You are a pragmatic wolf who works as a mercenary, taking jobs for the highest bidder. 
        You respect strength and value profit above all else. While powerful in combat, you 
        recognize the crow's magical knowledge could be useful. You speak confidently but are 
        always calculating the potential benefit of any situation."""
    )
}