//==============================================================================
//	
//	Copyright (c) 2002-
//	Authors:
//	* Andrew Hinton <ug60axh@cs.bham.ac.uk> (University of Birmingham)
//	* Dave Parker <david.parker@comlab.ox.ac.uk> (University of Oxford, formerly University of Birmingham)
//	
//------------------------------------------------------------------------------
//	
//	This file is part of PRISM.
//	
//	PRISM is free software; you can redistribute it and/or modify
//	it under the terms of the GNU General Public License as published by
//	the Free Software Foundation; either version 2 of the License, or
//	(at your option) any later version.
//	
//	PRISM is distributed in the hope that it will be useful,
//	but WITHOUT ANY WARRANTY; without even the implied warranty of
//	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//	GNU General Public License for more details.
//	
//	You should have received a copy of the GNU General Public License
//	along with PRISM; if not, write to the Free Software Foundation,
//	Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//	
//==============================================================================

package userinterface.model.computation;

import javax.swing.*;

import io.ModelExportTask;
import userinterface.*;
import userinterface.model.*;
import userinterface.util.*;

/**
 * Thread that performs transient probability computation on a model.
 */
public class ComputeTransientThread extends GUIComputationThread
{
	@SuppressWarnings("unused")
	private GUIMultiModelHandler handler;
	private String transientTimeSpec;
	private ModelExportTask exportTask;

	/** Creates a new instance of ComputeTransientThread */
	public ComputeTransientThread(GUIMultiModelHandler handler, String transientTimeSpec, ModelExportTask exportTask)
	{
		super(handler.getGUIPlugin());
		this.handler = handler;
		this.transientTimeSpec = transientTimeSpec;
		this.exportTask = exportTask;
	}

	public void run()
	{
		// Notify the interface that we are starting computation
		SwingUtilities.invokeLater(new Runnable()
		{
			public void run()
			{
				plug.startProgress();
				plug.notifyEventListeners(new GUIComputationEvent(GUIComputationEvent.COMPUTATION_START, plug));
				plug.setTaskBarText("Computing transient probabilities...");
			}
		});

		// Do Computation
		try {
			prism.exportTransientProbabilities(transientTimeSpec, exportTask.getFile(), exportTask.getExportOptions(), null);
		} catch (Throwable e) {
			error(e);
			SwingUtilities.invokeLater(new Runnable()
			{
				public void run()
				{
					plug.notifyEventListeners(new GUIComputationEvent(GUIComputationEvent.COMPUTATION_ERROR, plug));
					plug.setTaskBarText("Computing transient probabilities... error.");
					plug.stopProgress();
				}
			});
			return;
		}

		//If we get here, computation was successful
		SwingUtilities.invokeLater(new Runnable()
		{
			public void run()
			{
				plug.setTaskBarText("Computing transient probabilities... done.");
				plug.notifyEventListeners(new GUIComputationEvent(GUIComputationEvent.COMPUTATION_DONE, plug));
				plug.stopProgress();
			}
		});
	}
}
