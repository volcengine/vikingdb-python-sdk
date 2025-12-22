# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""Viking Memory Collection Class"""

import json
from .types import EnumEncoder


class Collection:
    """
    Viking Memory Collection operation class
    
    Simplifies operations on a single collection through object encapsulation
    """
    
    def __init__(self, client, collection_name=None, project_name="default", resource_id=None):
        """
        Initialize collection object
        
        This supports two usage patterns:
        1. Using collection_name and project_name to identify the collection
        2. Using resource_id directly to identify the collection uniquely
        
        Args:
            client (VikingMem): VikingMem instance
            collection_name (str, optional): Collection name. Required when not using resource_id.
            project_name (str, optional): Project name. Defaults to "default".
            resource_id (str, optional): Resource ID. When provided, takes precedence over collection_name/project_name.
            
        Raises:
            ValueError: When neither collection_name nor resource_id is provided.
        """
        if resource_id is None and collection_name is None:
            raise ValueError(
                "Either 'collection_name' or 'resource_id' must be provided to identify the collection"
            )
        
        self.client = client
        self.collection_name = collection_name
        self.project_name = project_name
        self.resource_id = resource_id
    
    # ==================== Event Operations ====================
    
    def add_event(
        self, 
        event_type, 
        memory_info, 
        user_id=None, 
        assistant_id=None, 
        group_id=None, 
        headers=None,
        timeout=None,
        update_profiles=None,
    ):
        """
        Add an event to the collection
        
        Args:
            event_type (str): Event type
            memory_info (dict): Memory information
            user_id (str, optional): User ID
            assistant_id (str, optional): Assistant ID
            group_id (str, optional): Group ID
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            update_profiles (optional): Profiles to update along with the event
            
        Returns:
            dict: Event information
        """
        params = {
            "event_type": event_type,
            "memory_info": memory_info
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if user_id is not None:
            params["user_id"] = user_id
        if assistant_id is not None:
            params["assistant_id"] = assistant_id
        if group_id is not None:
            params["group_id"] = group_id
        if update_profiles is not None:
            params["update_profiles"] = update_profiles
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = self.client.json_exception("AddEvent", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    async def async_add_event(
        self, 
        event_type, 
        memory_info, 
        user_id=None, 
        assistant_id=None, 
        group_id=None, 
        headers=None,
        timeout=None,
        update_profiles=None,
    ):
        """
        Add an event to the collection asynchronously
        
        Args:
            event_type (str): Event type
            memory_info (dict): Memory information
            user_id (str, optional): User ID
            assistant_id (str, optional): Assistant ID
            group_id (str, optional): Group ID
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            update_profiles (optional): Profiles to update along with the event
            
        Returns:
            dict: Event information
        """
        params = {
            "event_type": event_type,
            "memory_info": memory_info
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if user_id is not None:
            params["user_id"] = user_id
        if assistant_id is not None:
            params["assistant_id"] = assistant_id
        if group_id is not None:
            params["group_id"] = group_id
        if update_profiles is not None:
            params["update_profiles"] = update_profiles
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = await self.client.async_json_exception("AddEvent", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    def update_event(
        self, 
        event_id, 
        memory_info, 
        user_id=None, 
        assistant_id=None, 
        headers=None,
        timeout=None
    ):
        """
        Update an existing event
        
        Args:
            event_id (str): Event ID to update
            memory_info (dict): Updated memory information
            user_id (str, optional): User ID
            assistant_id (str, optional): Assistant ID
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Updated event information
        """
        params = {
            "event_id": event_id,
            "memory_info": memory_info
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if user_id is not None:
            params["user_id"] = user_id
        if assistant_id is not None:
            params["assistant_id"] = assistant_id
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = self.client.json_exception("UpdateEvent", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    async def async_update_event(
        self, 
        event_id, 
        memory_info, 
        user_id=None, 
        assistant_id=None, 
        headers=None,
        timeout=None
    ):
        """
        Update an existing event asynchronously
        
        Args:
            event_id (str): Event ID to update
            memory_info (dict): Updated memory information
            user_id (str, optional): User ID
            assistant_id (str, optional): Assistant ID
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Updated event information
        """
        params = {
            "event_id": event_id,
            "memory_info": memory_info
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if user_id is not None:
            params["user_id"] = user_id
        if assistant_id is not None:
            params["assistant_id"] = assistant_id
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = await self.client.async_json_exception("UpdateEvent", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    def delete_event(
        self, 
        event_id, 
        headers=None,
        timeout=None
    ):
        """
        Delete an event by ID
        
        Args:
            event_id (str): Event ID to delete
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Deletion result
        """
        params = {
            "event_id": event_id
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = self.client.json_exception("DeleteEvent", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    async def async_delete_event(
        self, 
        event_id, 
        headers=None,
        timeout=None
    ):
        """
        Delete an event by ID asynchronously
        
        Args:
            event_id (str): Event ID to delete
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Deletion result
        """
        params = {
            "event_id": event_id
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = await self.client.async_json_exception("DeleteEvent", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    def batch_delete_event(
        self, 
        filter=None,
        delete_type=None,
        headers=None,
        timeout=None
    ):
        """
        Batch delete events based on filter criteria
        
        Args:
            filter (dict, optional): Filter parameters. May contain event_type, user_id, assistant_id, start_time, end_time
            delete_type (str, optional): Delete type
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Batch deletion result
        """
        params = {}
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if delete_type is not None:
            params["delete_type"] = delete_type
        if filter is not None:
            params["filter"] = filter
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = self.client.json_exception("BatchDeleteEvent", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    async def async_batch_delete_event(
        self, 
        filter=None,
        delete_type=None,
        headers=None,
        timeout=None
    ):
        """
        Batch delete events based on filter criteria asynchronously
        
        Args:
            filter (dict, optional): Filter parameters. May contain event_type, user_id, assistant_id, start_time, end_time
            delete_type (str, optional): Delete type
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Batch deletion result
        """
        params = {}
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if delete_type is not None:
            params["delete_type"] = delete_type
        if filter is not None:
            params["filter"] = filter
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = await self.client.async_json_exception("BatchDeleteEvent", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    # ==================== Profile Operations ====================
    
    def add_profile(
        self, 
        profile_type, 
        memory_info, 
        user_id=None, 
        assistant_id=None, 
        group_id=None, 
        is_upsert=False, 
        headers=None,
        timeout=None
    ):
        """
        Add a profile to the collection
        
        Args:
            profile_type (str): Profile type
            memory_info (dict): Memory information
            user_id (str, optional): User ID
            assistant_id (str, optional): Assistant ID
            group_id (str, optional): Group ID
            is_upsert (bool, optional): Whether to upsert (insert or update). Defaults to False.
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Profile information
        """
        params = {
            "profile_type": profile_type,
            "memory_info": memory_info,
            "is_upsert": is_upsert
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if user_id is not None:
            params["user_id"] = user_id
        if assistant_id is not None:
            params["assistant_id"] = assistant_id
        if group_id is not None:
            params["group_id"] = group_id
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = self.client.json_exception("AddProfile", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    async def async_add_profile(
        self, 
        profile_type, 
        memory_info, 
        user_id=None, 
        assistant_id=None, 
        group_id=None, 
        is_upsert=False, 
        headers=None,
        timeout=None
    ):
        """
        Add a profile to the collection asynchronously
        
        Args:
            profile_type (str): Profile type
            memory_info (dict): Memory information
            user_id (str, optional): User ID
            assistant_id (str, optional): Assistant ID
            group_id (str, optional): Group ID
            is_upsert (bool, optional): Whether to upsert (insert or update). Defaults to False.
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Profile information
        """
        params = {
            "profile_type": profile_type,
            "memory_info": memory_info,
            "is_upsert": is_upsert
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if user_id is not None:
            params["user_id"] = user_id
        if assistant_id is not None:
            params["assistant_id"] = assistant_id
        if group_id is not None:
            params["group_id"] = group_id
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = await self.client.async_json_exception("AddProfile", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    def update_profile(
        self, 
        profile_id, 
        memory_info, 
        headers=None,
        timeout=None
    ):
        """
        Update an existing profile
        
        Args:
            profile_id (str): Profile ID to update
            memory_info (dict): Updated memory information
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Updated profile information
        """
        params = {
            "profile_id": profile_id,
            "memory_info": memory_info
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = self.client.json_exception("UpdateProfile", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    async def async_update_profile(
        self, 
        profile_id, 
        memory_info, 
        headers=None,
        timeout=None
    ):
        """
        Update an existing profile asynchronously
        
        Args:
            profile_id (str): Profile ID to update
            memory_info (dict): Updated memory information
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Updated profile information
        """
        params = {
            "profile_id": profile_id,
            "memory_info": memory_info
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = await self.client.async_json_exception("UpdateProfile", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res

    def delete_profile(
        self, 
        profile_id, 
        headers=None,
        timeout=None
    ):
        """
        Delete a profile by ID
        
        Args:
            profile_id (str): Profile ID to delete
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Deletion result
        """
        params = {
            "profile_id": profile_id
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = self.client.json_exception("DeleteProfile", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    async def async_delete_profile(
        self, 
        profile_id, 
        headers=None,
        timeout=None
    ):
        """
        Delete a profile by ID asynchronously
        
        Args:
            profile_id (str): Profile ID to delete
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Deletion result
        """
        params = {
            "profile_id": profile_id
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = await self.client.async_json_exception("DeleteProfile", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res

    def trigger_update_profile(
        self,
        update_profile_type=None,
        filters=None,
        headers=None,
        timeout=None,
    ):
        """
        Trigger profile update tasks for the collection
        
        Args:
            update_profile_type (list|str, optional): Profile types to update
            filters (dict, optional): Filter conditions, e.g., user_id, end_time
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
        
        Returns:
            dict: Trigger result
        """
        params = {}
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if update_profile_type is not None:
            params["update_profile_type"] = update_profile_type
        if filters is not None:
            params["filters"] = filters
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = self.client.json_exception("TriggerUpdateProfile", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res

    async def async_trigger_update_profile(
        self,
        update_profile_type=None,
        filters=None,
        headers=None,
        timeout=None,
    ):
        """
        Trigger profile update tasks for the collection asynchronously
        """
        params = {}
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if update_profile_type is not None:
            params["update_profile_type"] = update_profile_type
        if filters is not None:
            params["filters"] = filters
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = await self.client.async_json_exception("TriggerUpdateProfile", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    def batch_delete_profile(
        self, 
        filter=None,
        headers=None,
        timeout=None
    ):
        """
        Batch delete profiles based on filter criteria
        
        Args:
            filter (dict, optional): Filter parameters. May contain profile_type, user_id, assistant_id
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Batch deletion result
        """
        params = {}
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if filter is not None:
            params["filter"] = filter
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = self.client.json_exception("BatchDeleteProfile", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    async def async_batch_delete_profile(
        self, 
        filter=None,
        headers=None,
        timeout=None
    ):
        """
        Batch delete profiles based on filter criteria asynchronously
        
        Args:
            filter (dict, optional): Filter parameters. May contain profile_type, user_id, assistant_id
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Batch deletion result
        """
        params = {}
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if filter is not None:
            params["filter"] = filter
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = await self.client.async_json_exception("BatchDeleteProfile", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    # ==================== Session Operations ====================
    
    def add_session(
        self, 
        session_id, 
        messages, 
        metadata=None, 
        profiles=None,
        headers=None,
        timeout=None,
        store_file=None
    ):
        """
        Add session messages to the collection
        
        Args:
            session_id (str): Session ID
            messages (list): List of messages
            metadata (dict, optional): Session metadata
            profiles (list, optional): List of profiles
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Session information
        """
        params = {
            "session_id": session_id,
            "messages": messages,
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if metadata is not None:
            params["metadata"] = metadata
        if profiles is not None:
            params["profiles"] = profiles
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id
        if store_file is not None:
            params["store_file"] = store_file

        res = self.client.json_exception("AddSession", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    async def async_add_session(
        self, 
        session_id, 
        messages, 
        metadata=None, 
        profiles=None,
        headers=None,
        timeout=None,
        store_file=None
    ):
        """
        Add session messages to the collection asynchronously
        
        Args:
            session_id (str): Session ID
            messages (list): List of messages
            metadata (dict, optional): Session metadata
            profiles (list, optional): List of profiles
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Session information
        """
        params = {
            "session_id": session_id,
            "messages": messages,
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if metadata is not None:
            params["metadata"] = metadata
        if profiles is not None:
            params["profiles"] = profiles
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id
        if store_file is not None:
            params["store_file"] = store_file

        res = await self.client.async_json_exception("AddSession", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    # ==================== Session Info Operations ====================

    def get_session_info(
        self,
        session_id,
        headers=None,
        timeout=None
    ):
        """
        Get session information by session ID
        
        Args:
            session_id (str): Session ID to retrieve
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Session information
        """
        params = {
            "session_id": session_id
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = self.client.json_exception("GetSessionInfo", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    async def async_get_session_info(
        self,
        session_id,
        headers=None,
        timeout=None
    ):  
        """
        Get session information by session ID asynchronously
        
        Args:
            session_id (str): Session ID to retrieve
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Session information
        """
        params = {
            "session_id": session_id
        }
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = await self.client.async_json_exception("GetSessionInfo", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    # ==================== Search Operations ====================
    
    def search_memory(
        self, 
        query=None, 
        filter=None, 
        limit=None, 
        headers=None,
        timeout=None
    ):
        """
        Search memories in the collection
        
        Args:
            query (str, optional): Query text for semantic search
            filter (dict, optional): Filter parameters to narrow down results
            limit (int, optional): Maximum number of results to return
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Search results containing memory information
        """
        params = {}
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if query is not None:
            params["query"] = query
        if filter is not None:
            params["filter"] = filter
        if limit is not None:
            params["limit"] = limit
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = self.client.json_exception("SearchMemory", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    async def async_search_memory(
        self, 
        query=None, 
        filter=None, 
        limit=None, 
        headers=None,
        timeout=None
    ):
        """
        Search memories in the collection asynchronously
        
        Args:
            query (str, optional): Query text for semantic search
            filter (dict, optional): Filter parameters to narrow down results
            limit (int, optional): Maximum number of results to return
            headers (dict, optional): Custom request headers
            timeout (int, optional): Timeout in seconds
            
        Returns:
            dict: Search results containing memory information
        """
        params = {}
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if query is not None:
            params["query"] = query
        if filter is not None:
            params["filter"] = filter
        if limit is not None:
            params["limit"] = limit
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = await self.client.async_json_exception("SearchMemory", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res
    
    def search_event_memory(
        self,
        query=None,
        filter=None,
        time_decay_config=None,
        limit=None,
        headers=None,
        timeout=None
    ):
        params = {}
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if query is not None:
            params["query"] = query
        if filter is not None:
            params["filter"] = filter
        if time_decay_config is not None:
            params["time_decay_config"] = time_decay_config
        if limit is not None:
            params["limit"] = limit
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = self.client.json_exception("SearchEventMemory", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res

    def search_profile_memory(
        self,
        query=None,
        filter=None,
        limit=None,
        headers=None,
        timeout=None
    ):
        params = {}
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if query is not None:
            params["query"] = query
        if filter is not None:
            params["filter"] = filter
        if limit is not None:
            params["limit"] = limit
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = self.client.json_exception("SearchProfileMemory", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res

    async def async_search_event_memory(
        self,
        query=None,
        filter=None,
        time_decay_config=None,
        limit=None,
        headers=None,
        timeout=None
    ):
        """
        Search event memories in the collection asynchronously
        """
        params = {}
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if query is not None:
            params["query"] = query
        if filter is not None:
            params["filter"] = filter
        if time_decay_config is not None:
            params["time_decay_config"] = time_decay_config
        if limit is not None:
            params["limit"] = limit
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = await self.client.async_json_exception("SearchEventMemory", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res

    async def async_search_profile_memory(
        self,
        query=None,
        filter=None,
        limit=None,
        headers=None,
        timeout=None
    ):
        """
        Search profile memories in the collection asynchronously
        """
        params = {}
        if self.collection_name is not None:
            params["collection_name"] = self.collection_name
        if self.project_name is not None:
            params["project_name"] = self.project_name
        if query is not None:
            params["query"] = query
        if filter is not None:
            params["filter"] = filter
        if limit is not None:
            params["limit"] = limit
        if self.resource_id is not None:
            params["resource_id"] = self.resource_id

        res = await self.client.async_json_exception("SearchProfileMemory", {}, json.dumps(params, cls=EnumEncoder), headers=headers, timeout=timeout)
        return res

    
